import customtkinter as ctk


def create_stylish_button(
    master,
    text,
    command=None,
    font=None,
    fontsize=None,
    fg_color=None,
    hover_color=None,
    width=None,
    height=None,
    corner_radius=None,
):
    if font is None:
        font = 'Rubik bold'
    if fontsize is None:
        fontsize = 20
    if fg_color is None:
        fg_color = '#5429FE'
    if hover_color is None:
        hover_color = '#4a1e9e'
    if width is None:
        width = 147
    if height is None:
        height = 89
    if corner_radius is None:
        corner_radius = 20
    return ctk.CTkButton(
        master=master,
        command=command,
        text=text,
        font=(font, fontsize),
        fg_color=fg_color,
        hover_color=hover_color,
        width=width,
        height=height,
        corner_radius=corner_radius,
    )
