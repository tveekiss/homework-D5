from django_filters import FilterSet, ModelChoiceFilter, DateTimeFilter
from django.forms import DateTimeInput
import django_filters as filters
from .models import Post, Category


class PostFilters(FilterSet):
    title = filters.CharFilter(label='название', lookup_expr='icontains')
    category = ModelChoiceFilter(
        field_name="categories",
        queryset=Category.objects.all(),
        label='Категория',
        empty_label='Все'

    )
    date = DateTimeFilter(
        field_name='date',
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        ),
        label='дата публикации'
    )