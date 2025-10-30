"""
KnowledgeGraphMemory
- Stores and queries relationships between products, styles, trends, and client preferences.
- Uses Neo4j (or can be adapted to SQLite with relationships).
"""
from typing import Any
try:
    from neo4j import GraphDatabase
except ImportError:
    GraphDatabase = None

class KnowledgeGraphMemory:
    def __init__(self, uri=None, user=None, password=None):
        if GraphDatabase and uri and user and password:
            self.driver = GraphDatabase.driver(uri, auth=(user, password))
        else:
            self.driver = None

    def add_product(self, name: str, style: str, price: float, brand: str):
        if not self.driver:
            return False
        with self.driver.session() as session:
            session.run(
                """MERGE (p:Product {name: $name, style: $style, price: $price, brand: $brand})""",
                name=name, style=style, price=price, brand=brand
            )
        return True

    def add_relationship(self, from_label: str, from_name: str, to_label: str, to_name: str, rel_type: str):
        if not self.driver:
            return False
        with self.driver.session() as session:
            session.run(
                f"""
                MATCH (a:{from_label} {{name: $from_name}}), (b:{to_label} {{name: $to_name}})
                MERGE (a)-[r:{rel_type}]->(b)
                """,
                from_name=from_name, to_name=to_name
            )
        return True

    def query(self, cypher: str) -> Any:
        if not self.driver:
            return None
        with self.driver.session() as session:
            return session.run(cypher).data()
