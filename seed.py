import models

models.db.create_db_and_tables()

with models.db.Session(models.db.engine) as s:
    cat1 = models.Category(c_name="Toy")
    cat2 = models.Category(c_name="Food")
    s.add(cat1)
    s.add(cat2)
    s.add(
        models.Product(
            p_name="SuperHero",
            price="19.99",
            category=cat1,
        )
    )
    s.add(models.Product(p_name="Potato", price="5.99", category=cat2))
    s.add(
        models.Product(
            p_name="Ketchup",
            price="3.99",
            category=cat2,
        )
    )
    s.commit()
