from geopy.distance import geodesic

def select_top_volunteers(volunteer_dict, ward_location, required_volunteers=2):
    volunteers = []

    for vid, info in volunteer_dict.items():
        distance_km = geodesic(info["location"], ward_location).km
        volunteers.append({
            "id": vid,
            "audit_score": info["audit_score"],
            "distance_km": distance_km
        })

    max_audit = max(v["audit_score"] for v in volunteers)
    for v in volunteers:
        v["inv_distance"] = 1 / (v["distance_km"] + 1)

    inv_distances = [v["inv_distance"] for v in volunteers]
    min_inv, max_inv = min(inv_distances), max(inv_distances)

    for v in volunteers:
        v["norm_distance_score"] = (
            (v["inv_distance"] - min_inv) / (max_inv - min_inv)
            if max_inv != min_inv else 1.0
        )
        v["norm_score"] = v["audit_score"] / max_audit if max_audit != 0 else 0

    ALPHA = 0.7
    BETA = 0.3
    for v in volunteers:
        v["final_score"] = (
            ALPHA * v["norm_distance_score"] +
            BETA * v["norm_score"]
        )

    sorted_volunteers = sorted(volunteers, key=lambda x: x["final_score"], reverse=True)
    selected_ids = [v["id"] for v in sorted_volunteers[:required_volunteers]]

    return selected_ids
