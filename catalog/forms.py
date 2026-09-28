from catalog.models import Product
from django import forms

FORBIDDEN_WORDS = [
    "казино",
    "криптовалюта",
    "крипта",
    "биржа",
    "дешево",
    "бесплатно",
    "обман",
    "полиция",
    "радар",
]


class ProductForm(forms.ModelForm):
    """Форма для создания и редактирования продукта"""

    class Meta:
        model = Product
        fields = ["name", "description", "image", "category", "price"]

    def __init__(self, *args, **kwargs):
        """Стилизация формы под Bootstrap"""
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if field_name == "is_published":
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"

    def clean_name(self):
        """Валидация поля name — проверка на запрещённые слова"""
        name = self.cleaned_data.get("name", "").lower()
        for word in FORBIDDEN_WORDS:
            if word in name:
                raise forms.ValidationError(f'Слово "{word}" запрещено использовать в названии.')
        return name

    def clean_description(self):
        """Валидация поля description — проверка на запрещённые слова"""
        description = self.cleaned_data.get("description", "").lower()
        for word in FORBIDDEN_WORDS:
            if word in description:
                raise forms.ValidationError(f'Слово "{word}" запрещено использовать в описании.')
        return description

    def clean_price(self):
        """Валидация поля price — проверка на отрицательную цену"""
        price = self.cleaned_data.get("price")
        if price is not None and price < 0:
            raise forms.ValidationError("Цена не может быть отрицательной!")
        return price
