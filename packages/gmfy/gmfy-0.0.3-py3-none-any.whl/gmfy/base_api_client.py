class GMFYApiClientBase:
    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json",
        }
        self.urls = {
            "post_event": f"{self.base_url}v1/events/",
            "post_events": f"{self.base_url}v1/events/batch/",
            "post_payment": f"{self.base_url}v1/payments/",
            "resend_code": f"{self.base_url}v1/payments/{{payment_id}}/resend-code/",
            "get_version": f"{self.base_url}v1/version/",
            "get_user": f"{self.base_url}v1/users/{{user_id}}/",
            "get_users": f"{self.base_url}v1/users/",
            "get_ratings": f"{self.base_url}v1/ratings/{{rating_id}}/top/",
            "get_challenges": f"{self.base_url}v1/challenges/{{challenge_id}}/top/",
            "get_badges": f"{self.base_url}v1/badges/{{user_id}}/",
            "get_notifications": f"{self.base_url}v1/notifications/",
            "get_unread_notifications": f"{self.base_url}v1/notifications/unread/",
            "get_unread_notifications_user": (
                f"{self.base_url}v1/notifications/unread/{{user_id}}/"
            ),
            "get_payment": f"{self.base_url}v1/payments/{{payment_id}}/",
        }
