# scripts/hero_roles.py

# Dictionary mapping hero IDs to roles
hero_roles = {
    1: "carry",
    2: "support",
    # Add all other heroes and their roles
}

def get_role(hero_id):
    return hero_roles.get(hero_id, "unknown")

if __name__ == "__main__":
    hero_id = 1  # Example hero ID
    role = get_role(hero_id)
    print(f"Hero {hero_id} plays as {role}")
