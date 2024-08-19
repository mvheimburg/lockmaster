import flet as ft

class Login(ft.UserControl):
  def __init__(self, page):
    # super().__init__()
    self.page = page

  def build(self):
    return ft.Column(
      controls=[
        ft.Container(
          height=800,width=200,
          bgcolor='blue',
          content=ft.Column(
            controls=[
              ft.Text('Welcome back \n This is the login pages'),
              ft.Container(
                on_click= lambda _: self.page.go('/'), 
                content=ft.Text('Goto Home',size=25,color='black')
              )
            ]
          )
          )
        ]
    )