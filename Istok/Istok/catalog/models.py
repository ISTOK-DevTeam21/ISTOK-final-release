from django.db import models
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    """
    Модель для категорий продуктов.

    Attributes:
        name (str): Название категории.
        description (str): Описание категории (необязательное поле).
    """

    name = models.CharField(max_length=255, unique=True, verbose_name=_('Название'))
    description = models.TextField(blank=True, verbose_name=_('Описание'))

    class Meta:
        verbose_name = _('Категория')
        verbose_name_plural = _('Категории')

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Модель для продуктов.

    Attributes:
        name (str): Название продукта.
        description (str): Описание продукта.
        material_facade(str): Материал фасада.
        material_table_top(str): Материал столешницы.
        material_apron(str): Материал фартука.
        style(str): Стиль продукта.
        price (Decimal): Цена продукта.
        categories (Category): Категории, к которым относится продукт.
        is_active (bool): Флаг активности продукта.
        created_at (DateTime): Дата и время создания продукта.
        updated_at (DateTime): Дата и время последнего обновления продукта.
    """

    MATERIAL_FACADE = [
        ('mdf_cpf_plastic', _('МДФ + CPL пластик')),
        ('mdf_pvx_tape', _('МДФ + ПВХ пленка')),
        ('mdf_enamel', _('МДФ + Эмаль'))
    ]

    MATERIAL_TABLE_TOP = [
        ('hpl_compact', _('HPL - компакт')),
        ('dsp', _('ДСП'))
    ]

    MATERIAL_APRON = [
        ('dsp', _('ДСП'))
    ]

    STYLES = [
        ('classic', _('Классика')),
        ('minimalism', _('Минимализм')),
        ('modern', _('Модерн')),
        ('scandinavian', _('Скандинавский')),
        ('simple', _('Простой'))
    ]

    name = models.CharField(max_length=255, verbose_name=_('Название'))
    description = models.TextField(verbose_name=_('Описание'))
    material_facade = models.CharField(max_length=255,
                                       choices=MATERIAL_FACADE,
                                       default='mdf_cpf_plastic',
                                       verbose_name=_('Материал фасада')
                                       )
    material_table_top = models.CharField(max_length=255,
                                          choices=MATERIAL_TABLE_TOP,
                                          default='hpl_compact',
                                          verbose_name=_('Материал столешницы')
                                          )
    material_apron = models.CharField(max_length=255,
                                      choices=MATERIAL_APRON,
                                      default='dsp',
                                      verbose_name=_('Материал фартука')
                                      )
    style = models.CharField(max_length=255,
                             choices=STYLES,
                             default='classic',
                             verbose_name=_('Стиль')
                             )
    sketchfab_embed = models.TextField(blank=True, verbose_name=_('Код для встраивания Sketchfab'))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Цена'))
    categories = models.ManyToManyField(Category, related_name='products', verbose_name=_('Категории'))
    is_active = models.BooleanField(default=True, verbose_name=_('Активный'))
    is_catalog = models.BooleanField(default=True, verbose_name=_('В каталоге'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата создания'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Дата обновления'))

    class Meta:
        verbose_name = _('Продукт')
        verbose_name_plural = _('Продукты')

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    """
    Модель для изображений продуктов.

    Attributes:
        product (Product): Продукт, к которому относится изображение.
        image (Image): Изображение продукта.
    """

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name=_('Продукт'))
    image = models.ImageField(upload_to='static/product_images/', verbose_name=_('Изображение'))

    class Meta:
        verbose_name = _('Изображение продукта')
        verbose_name_plural = _('Изображения продуктов')

    def __str__(self):
        return f'Изображение {self.product.name}'


class Promotion(models.Model):
    """
    Модель для акции.

    Attributes:
        name (str): Название акции.
        description (str): Описание акции.
        start_date (DateTime): Дата начала акции.
        end_date (DateTime): Дата окончания акции.
        is_active (bool): Флаг активности акции.
    """

    name = models.CharField(max_length=255, verbose_name=_('Название'))
    description = models.TextField(verbose_name=_('Описание'))
    start_date = models.DateTimeField(verbose_name=_('Дата начала'))
    end_date = models.DateTimeField(verbose_name=_('Дата окончания'))
    is_active = models.BooleanField(default=True, verbose_name=_('Активная'))

    class Meta:
        verbose_name = _('Акция')
        verbose_name_plural = _('Акции')

    def __str__(self):
        return self.name


class PromotionImage(models.Model):
    """
    Модель для изображений акции.

    Attributes:
        promotion (Promotion): Акция, к которой относится изображение.
        image (Image): Изображение акции.
    """

    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE, related_name='images', verbose_name=_('Акция'))
    image = models.ImageField(upload_to='promotion_images/', verbose_name=_('Изображение'), blank=True)

    class Meta:
        verbose_name = _('Изображение акции')
        verbose_name_plural = _('Изображения акции')

    def __str__(self):
        return f'Изображение {self.promotion.name}'
