from rest_framework import routers
from fruits.viewsets import FruitViewSets

router = routers.SimpleRouter()

# ##################################################################### #
# ################### Fruits                    ###################### #
# ##################################################################### #

router.register(r"fruits", FruitViewSets, basename="fruits")


urlpatterns = [
    *router.urls,
]
