from django.forms import widgets


class GeojsonMapWidget(widgets.Textarea):
    template_name = "business/widgets/map_editor.html"

    class Media:
        css = {
            "all": ("core/_css/tailwind/output.css", "core/_css/admin.css"),
        }
