from django.urls import reverse
from django.utils.html import format_html
from unfold.decorators import display


def render_action_buttons(obj, edit_label="ویرایش", delete_label="حذف"):
    opts = obj._meta
    change_url = reverse(f"admin:{opts.app_label}_{opts.model_name}_change", args=[obj.pk])
    delete_url = reverse(f"admin:{opts.app_label}_{opts.model_name}_delete", args=[obj.pk])
    return format_html(
        '<div class="flex items-center gap-1.5 justify-center flex-nowrap text-xs">'
        '<a href="{}" class="action-btn-edit inline-flex items-center gap-1 px-2.5 py-1 rounded-lg bg-teal-50 hover:bg-teal-100 text-teal-700 dark:bg-teal-950/60 dark:text-teal-300 font-bold transition-all hover:scale-105" title="{}">'
        '<span class="material-symbols-outlined text-sm leading-none">edit</span>'
        '<span>{}</span>'
        '</a>'
        '<a href="{}" class="action-btn-delete inline-flex items-center gap-1 px-2.5 py-1 rounded-lg bg-rose-50 hover:bg-rose-100 text-rose-700 dark:bg-rose-950/60 dark:text-rose-300 font-bold transition-all hover:scale-105" title="{}">'
        '<span class="material-symbols-outlined text-sm leading-none">delete</span>'
        '<span>{}</span>'
        '</a>'
        '</div>',
        change_url,
        edit_label,
        edit_label,
        delete_url,
        delete_label,
        delete_label
    )
