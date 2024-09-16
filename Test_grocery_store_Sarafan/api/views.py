from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import (CategorySerializer, ProductSerializer,
                             ShoppingCartItemSerializer,
                             ShoppingCartReadSerializer)
from groceries.models import Category, Product, ShoppingCartItem


class CategoryViewSet(viewsets.ModelViewSet):

    queryset = Category.objects.prefetch_related('subcategories').all()
    serializer_class = CategorySerializer
    http_method_names = ('get',)
    permission_classes = (AllowAny,)


class ProductViewSet(viewsets.ModelViewSet):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    http_method_names = ('get', 'post', 'delete',)
    permission_classes = (AllowAny,)

    @action(
        detail=True,
        methods=('post',),
        permission_classes=(IsAuthenticated,),
        url_path='shopping_cart_item'
    )
    def add_to_shopping_cart(self, request, pk=None):
        """
        Добавление или обновление продукта в корзине.
        """
        amount = request.data.get('amount', 1)
        data = {
            'user': request.user.id,
            'product': pk,
            'amount': amount
        }
        serializer = ShoppingCartItemSerializer(
            data=data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)

        shopping_cart_item = ShoppingCartItem.objects.filter(
            user=request.user,
            product=pk
        ).first()

        if shopping_cart_item:
            shopping_cart_item.amount += int(amount)
            shopping_cart_item.save()
            updated_serializer = ShoppingCartItemSerializer(
                shopping_cart_item,
                context={'request': request}
            )
            return Response(updated_serializer.data, status=status.HTTP_200_OK)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @add_to_shopping_cart.mapping.delete
    def remove_from_shopping_cart(self, request, pk=None):
        shopping_cart_item = ShoppingCartItem.objects.filter(
            user=request.user,
            product=pk
        )
        if shopping_cart_item.exists():
            shopping_cart_item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ShoppingCartAPIView(APIView):
    """
    Эндпоинт для получения состава и очистки карзины.
    """

    serializer_class = ShoppingCartReadSerializer

    def get_queryset(self):
        """
        Возвращает qureset товаров в корзине текущего пользователя.
        """
        return ShoppingCartItem.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(
            {
                'products': serializer.data,
                'total_cost': self.get_total_cost(queryset)
            },
            status=status.HTTP_200_OK
        )

    def get_total_cost(self, queryset):
        """
        Возвращает суммарную стоимость товаров в корзине.
        """
        return sum(item.product.price * item.amount for item in queryset)

    def delete(self, request):
        """
        Очищает корзину текущего пользователя.
        """
        self.get_queryset().delete()
        return Response(
            {
                'detail': 'Корзина очищена.'
            },
            status=status.HTTP_204_NO_CONTENT
        )
