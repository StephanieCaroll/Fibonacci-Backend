from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from fibonacci.models import Product, Order, OrderItem, ShippingAddress
from fibonacci.serializers import OrderSerializer

from datetime import datetime

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addOrderItems(request):
    user = request.user
    data = request.data
    
    print("=" * 50)
    print("📦 Dados recebidos no backend:")
    print(data)
    print("=" * 50)
    
    orderItems = data.get('orderItems', [])

    if not orderItems or len(orderItems) == 0:
        return Response({'detail': 'Nenhum item no pedido'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Calcular itemsPrice baseado nos itens
        itemsPrice = 0
        for item in orderItems:
            # TENTAR PEGAR O ID DO PRODUTO DE DIFERENTES FORMAS
            product_id = item.get('product') or item.get('_id') or item.get('id')
            
            print(f"🔍 Item: {item}")
            print(f"📌 Product ID encontrado: {product_id}")
            
            if not product_id:
                return Response({'detail': f'Produto sem ID: {item}'}, 
                              status=status.HTTP_400_BAD_REQUEST)
            
            # Buscar o produto
            try:
                product = Product.objects.get(_id=product_id)
                print(f"✅ Produto encontrado: {product.name}")
            except Product.DoesNotExist:
                return Response({'detail': f'Produto com ID {product_id} não encontrado'}, 
                              status=status.HTTP_404_NOT_FOUND)
            
            # Calcular preço
            price = float(item.get('price', 0))
            qty = int(item.get('qty', 1))
            itemsPrice += price * qty
        
        # Usar valores do frontend ou calcular
        taxPrice = float(data.get('taxPrice', 0))
        shippingPrice = float(data.get('shippingPrice', 0))
        totalPrice = float(data.get('totalPrice', itemsPrice + taxPrice + shippingPrice))
        
        print(f"💰 Preços calculados: itemsPrice={itemsPrice}, taxPrice={taxPrice}, shippingPrice={shippingPrice}, totalPrice={totalPrice}")
        
        # Criar o pedido
        order = Order.objects.create(
            user=user,
            paymentMethod=data.get('paymentMethod', 'Cartão'),
            taxPrice=taxPrice,
            shippingPrice=shippingPrice,
            totalPrice=totalPrice
        )
        print(f"✅ Pedido criado: ID {order._id}")

        # Criar endereço de entrega
        shipping_address = data.get('shippingAddress', {})
        ShippingAddress.objects.create(
            order=order,
            address=shipping_address.get('address', ''),
            city=shipping_address.get('city', ''),
            postalCode=shipping_address.get('postalCode', ''),
            country=shipping_address.get('country', ''),
        )
        print("✅ Endereço criado")

        # Processar cada item do pedido
        for item in orderItems:
            # Pegar ID do produto
            product_id = item.get('product') or item.get('_id') or item.get('id')
            product = Product.objects.get(_id=product_id)
            
            qty = int(item.get('qty', 1))
            
            # Verificar se o usuário é o dono da obra
            if product.user and product.user.id == user.id:
                order.delete() 
                return Response({'detail': f'Você é o autor de "{product.name}" e não pode comprá-la.'}, 
                              status=status.HTTP_400_BAD_REQUEST)

            # Verificar estoque
            if product.countInstock < qty:
                order.delete()
                return Response({'detail': f'Estoque insuficiente para "{product.name}". Disponível: {product.countInstock}'}, 
                              status=status.HTTP_400_BAD_REQUEST)

            image_url = ''
            if product.image:
                try:
                    if hasattr(product.image, 'url'):
                        image_url = product.image.url
                    else:
                        image_url = str(product.image)
                except:
                    image_url = ''

            # Criar item do pedido
            OrderItem.objects.create(
                product=product,
                order=order,
                name=product.name,
                qty=qty,
                price=float(item.get('price', product.price)),
                image=image_url
            )
            print(f"✅ Item criado: {product.name} x{qty}")

            # Atualizar estoque
            product.countInstock -= qty
            product.save()
            print(f"📦 Estoque atualizado: {product.name} agora tem {product.countInstock}")

        serializer = OrderSerializer(order, many=False)
        print("🎉 Pedido finalizado com sucesso!")
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        print(f"❌ ERRO CRÍTICO: {str(e)}")
        import traceback
        traceback.print_exc()
        return Response({'detail': f'Erro interno: {str(e)}'}, 
                      status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getOrderById(request, pk):
    user = request.user
    try:
        order = Order.objects.get(_id=pk)
        
        
        if user.is_staff or order.user == user:
            serializer = OrderSerializer(order, many=False)
            return Response(serializer.data)
        else:
            return Response({'detail': 'Não autorizado para visualizar este pedido'}, 
                            status=status.HTTP_401_UNAUTHORIZED)
            
    except Order.DoesNotExist:
        return Response({'detail': 'Pedido não encontrado'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateOrderToPaid(request, pk):
    try:
        order = Order.objects.get(_id=pk)
        
        
        order.isPaid = True
        order.paidAt = datetime.now()
        order.save()
        
        return Response({'detail': 'Pedido foi pago com sucesso!'}, status=status.HTTP_200_OK)
        
    except Order.DoesNotExist:
        return Response({'detail': 'Pedido não encontrado'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getMyOrders(request):
    user = request.user
    
    orders = user.order_set.all().order_by('-_id')
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)