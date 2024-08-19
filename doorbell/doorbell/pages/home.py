import flet as ft

class Home(ft.UserControl):
  
  def __init__(self, page):
    # super().__init__()
    self.page = page

  def build(self):
    return ft.Column(
      controls=[
        ft.Container(
          height=800,width=300,
          bgcolor='red',
          content=ft.Column(
            controls=[
              ft.Text('Welcome to the homepage'),
              ft.Container(
                on_click= lambda _: self.page.go('/login') ,
                content=ft.Text('Goto Login',size=25,color='black')
              )
            ]
          )
          )
        ]
    )