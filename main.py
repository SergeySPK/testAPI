from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI(title="Blue Sphere API")

# ВАЖНО: Разрешаем CORS, чтобы Flutter Web (localhost) мог делать запросы
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Для разработки разрешаем всё
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# 1. МОДЕЛИ ДАННЫХ (Точно как в Dart)
# ==========================================

class SchoolClass(BaseModel):
    id: str
    name: str

class LoadDay(BaseModel):
    day: int
    level: int # 0 - перегруз, 4 - пусто

class ClassStatus(BaseModel):
    level: int # 0 - перегруз, 4 - пусто
    date: str # формат "09.09"

class Recommendation(BaseModel):
    daysToReduce: List[int]
    daysToMoveTo: List[int]

class UserProfile(BaseModel):
    sferum_id: str
    role: str # "teacher" или "student"
    class_id: str

# ==========================================
# 2. МОК-ДАННЫЕ (Заглушки)
# ==========================================

# Генерируем классы как в mock_data.dart
mock_classes_db: Dict[str, List[SchoolClass]] = {}
for i in range(1, 12):
    mock_classes_db[f"{i} класс"] = [
        SchoolClass(id=f"{i}a", name=f"Класс {i}А"),
        SchoolClass(id=f"{i}b", name=f"Класс {i}Б"),
        SchoolClass(id=f"{i}v", name=f"Класс {i}В"),
        SchoolClass(id=f"{i}g", name=f"Класс {i}Г"),
        SchoolClass(id=f"{i}d", name=f"Класс {i}Д"),
    ]

# Генерируем календарь (уровни от 0 до 4)
mock_load_days = [
    LoadDay(day=1, level=1), LoadDay(day=2, level=1), LoadDay(day=3, level=0),
    LoadDay(day=4, level=0), LoadDay(day=5, level=2), LoadDay(day=6, level=3),
    LoadDay(day=7, level=2), LoadDay(day=8, level=1), LoadDay(day=9, level=0),
    LoadDay(day=10, level=0), LoadDay(day=11, level=1), LoadDay(day=12, level=2),
    LoadDay(day=13, level=4), LoadDay(day=14, level=1), LoadDay(day=15, level=0),
    LoadDay(day=16, level=0), LoadDay(day=17, level=2), LoadDay(day=18, level=3),
    LoadDay(day=19, level=2), LoadDay(day=20, level=1), LoadDay(day=21, level=0),
    LoadDay(day=22, level=0), LoadDay(day=23, level=1), LoadDay(day=24, level=2),
    LoadDay(day=25, level=2), LoadDay(day=26, level=4), LoadDay(day=27, level=0),
    LoadDay(day=28, level=0), LoadDay(day=29, level=1), LoadDay(day=30, level=2),
]

# ==========================================
# 3. ЭНДПОИНТЫ (API)
# ==========================================

@app.get("/api/classes", response_model=Dict[str, List[SchoolClass]])
async def get_classes():
    """
    Возвращает список классов, сгруппированных по параллелям.
    Фронт ожидает Map<String, List<SchoolClass>>.
    """
    return mock_classes_db

@app.get("/api/classes/{class_id}/heatmap", response_model=List[LoadDay])
async def get_heatmap(class_id: str, month: str = "09"):
    """
    Возвращает данные для календаря.
    """
    # Пока отдаем одни и те же данные для любого класса
    return mock_load_days

@app.get("/api/classes/{class_id}/summary", response_model=ClassStatus)
async def get_summary(class_id: str, date: str = "09.09"):
    """
    Возвращает статус класса на сегодня (для верхнего баннера).
    """
    return ClassStatus(level=4, date="09.09")

@app.get("/api/classes/{class_id}/recommendations", response_model=Recommendation)
async def get_recommendations(class_id: str):
    """
    Возвращает рекомендации от ИИ. Пока пустые массивы.
    """
    return Recommendation(daysToReduce=[], daysToMoveTo=[])

# ==========================================
# 4. АВТОРИЗАЦИЯ И РОЛИ (Ответ на пункт 5)
# ==========================================

@app.post("/api/auth", response_model=UserProfile)
async def auth_user(init_data: str):
    """
    Сюда фронт будет присылать initData из MAX.
    Пока мы просто имитируем проверку и возвращаем профиль учителя.
    В будущем здесь будет валидация HMAC-подписи и запрос в БД.
    """
    # TODO: Валидировать init_data через BOT_TOKEN
    
    # Заглушка: возвращаем тестового учителя
    return UserProfile(
        sferum_id="123456789",
        role="teacher",
        class_id="5b" # Учитель ведет 5Б
    )