from handlers.start import router as start_router
from handlers.tracker import router as tracker_router
from handlers.stats import router as stats_router

all_routers = [start_router, tracker_router, stats_router]
