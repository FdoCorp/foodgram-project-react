from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_auto_1712"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="user",
            options={
                "ordering": ["id"],
                "verbose_name": "Пользователь",
                "verbose_name_plural": "Пользователи",
            },
        ),
    ]
