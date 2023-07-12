from aiogram.fsm.state import StatesGroup,State



class FormStatrsGroup(StatesGroup):
    fill_name = State()
    fill_age = State()
    upload_photo = State()
