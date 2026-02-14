"""
AI/ML Recommendation Engine
Implements content-based filtering for heritage sites and artisans
Pure Python - no pandas/numpy for compatibility with all Python versions.
"""

from collections import Counter


class RecommendationEngine:
    """AI-powered recommendation system for heritage sites and artisans"""

    def __init__(self):
        pass

    def recommend_heritage_sites(self, sites_data, top_n=5):
        """Recommend top heritage sites by visitor count."""
        if not sites_data:
            return []
        sorted_sites = sorted(
            sites_data,
            key=lambda s: s.get('annual_visitors') or 0,
            reverse=True
        )
        return sorted_sites[:top_n]

    def recommend_artisans_by_state(self, artisans_data, state_filter=None, top_n=5):
        """Recommend artisans, optionally filtered by state, sorted by price (affordable first)."""
        if not artisans_data:
            return []
        if state_filter:
            artisans_data = [
                a for a in artisans_data
                if (a.get('state') or '').lower() == state_filter.lower()
            ]
        sorted_artisans = sorted(
            artisans_data,
            key=lambda a: a.get('product_price') or 0
        )
        return sorted_artisans[:top_n]

    def recommend_by_category(self, sites_data, category, top_n=3):
        """Recommend heritage sites by category."""
        if not sites_data or not category:
            return []
        filtered = [
            s for s in sites_data
            if (s.get('category') or '').lower() == category.lower()
        ]
        sorted_sites = sorted(
            filtered,
            key=lambda s: s.get('annual_visitors') or 0,
            reverse=True
        )
        return sorted_sites[:top_n]

    def get_state_wise_distribution(self, artisans_data):
        """State-wise artisan counts."""
        if not artisans_data:
            return {}
        states = [a.get('state') or '' for a in artisans_data]
        return dict(Counter(states))

    def get_visitor_trends(self, sites_data):
        """Top 10 sites by visitors for charts."""
        if not sites_data:
            return {'labels': [], 'values': []}
        sorted_sites = sorted(
            sites_data,
            key=lambda s: s.get('annual_visitors') or 0,
            reverse=True
        )[:10]
        return {
            'labels': [s.get('name') or '' for s in sorted_sites],
            'values': [s.get('annual_visitors') or 0 for s in sorted_sites]
        }

    def calculate_economic_impact(self, sites_data, artisans_data):
        """Economic impact metrics."""
        total_visitors = sum(s.get('annual_visitors', 0) or 0 for s in (sites_data or []))
        prices = [a.get('product_price', 0) or 0 for a in (artisans_data or [])]
        avg_product_price = sum(prices) / len(prices) if prices else 0
        tourism_revenue = total_visitors * 500
        artisan_revenue = len(artisans_data or []) * avg_product_price * 50
        return {
            'total_visitors': total_visitors,
            'tourism_revenue': tourism_revenue,
            'artisan_revenue': artisan_revenue,
            'total_economic_impact': tourism_revenue + artisan_revenue,
            'avg_product_price': avg_product_price
        }
