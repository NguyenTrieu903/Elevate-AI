"""Customer Support mock data for RAG chatbot system."""

from typing import List, Dict, Any

# Customer Support FAQ Documents
CUSTOMER_SUPPORT_DOCS = [
    {
        "page_content": "How to track my order? You can track your order using the order number sent to your email. Visit our website, go to 'Track Order' section, and enter your order number and email address. You'll see real-time updates on shipping status, estimated delivery date, and tracking information.",
        "metadata": {"source": "FAQ - Order Tracking", "category": "Orders", "priority": "high"}
    },
    {
        "page_content": "How to return or exchange items? Items can be returned within 30 days of purchase. Log into your account, go to 'My Orders', select the item to return, and print the prepaid return label. Original packaging and receipt are required. Exchanges for different sizes/colors are processed immediately upon receipt.",
        "metadata": {"source": "FAQ - Returns & Exchanges", "category": "Returns", "priority": "high"}
    },
    {
        "page_content": "What payment methods do you accept? We accept all major credit cards (Visa, MasterCard, American Express), PayPal, Apple Pay, Google Pay, and bank transfers. For large orders over $1000, we also accept purchase orders from verified business customers. All transactions are secure and encrypted.",
        "metadata": {"source": "FAQ - Payment Methods", "category": "Payments", "priority": "medium"}
    },
    {
        "page_content": "Shipping costs and delivery times: Standard shipping (5-7 business days) is $4.99 for orders under $50, free for orders over $50. Express shipping (2-3 business days) is $9.99. Next-day delivery is $19.99 and available in major cities. International shipping rates vary by destination.",
        "metadata": {"source": "FAQ - Shipping Information", "category": "Shipping", "priority": "high"}
    },
    {
        "page_content": "Product warranty information: All products come with manufacturer warranty. Electronics have 1-year warranty, clothing has 6-month warranty for defects. Extended warranty available at checkout. To claim warranty, contact support with order number and photos of the defective item.",
        "metadata": {"source": "FAQ - Warranty", "category": "Warranty", "priority": "medium"}
    },
    {
        "page_content": "How to cancel my order? Orders can be cancelled within 1 hour of placement if not yet processed. Log into your account, find the order, and click 'Cancel'. If already processed, you'll need to return the items after delivery. Refunds are processed within 3-5 business days.",
        "metadata": {"source": "FAQ - Order Cancellation", "category": "Orders", "priority": "medium"}
    },
    {
        "page_content": "Product availability and stock: Our website shows real-time inventory. 'In Stock' items ship within 1 business day. 'Low Stock' items have less than 5 units available. 'Pre-order' items are coming soon. Sign up for restock notifications to be notified when out-of-stock items return.",
        "metadata": {"source": "FAQ - Product Availability", "category": "Inventory", "priority": "medium"}
    },
    {
        "page_content": "How to use discount codes and coupons? Enter coupon code at checkout in the 'Promo Code' field before payment. Codes are case-sensitive. Some restrictions apply - check code terms. Only one code per order. Codes cannot be combined with other offers. Contact support if code isn't working.",
        "metadata": {"source": "FAQ - Discount Codes", "category": "Promotions", "priority": "low"}
    },
    {
        "page_content": "Account and profile management: Create account for faster checkout and order tracking. Update profile information in 'My Account' section. Change password, update shipping addresses, and manage payment methods. Delete account option available in account settings with data export option.",
        "metadata": {"source": "FAQ - Account Management", "category": "Account", "priority": "low"}
    },
    {
        "page_content": "Customer support contact information: Email support@company.com for non-urgent issues (24-48 hour response). Call 1-800-SUPPORT for immediate assistance (Mon-Fri 8AM-8PM EST). Live chat available on website during business hours. Premium customers get priority support.",
        "metadata": {"source": "FAQ - Contact Support", "category": "Support", "priority": "high"}
    }
]

# Customer Order Database
CUSTOMER_ORDERS_DB = {
    "ORD123456": {
        "status": "Shipped",
        "items": ["Wireless Headphones", "Phone Case"],
        "tracking": "1Z999AA1234567890",
        "estimated_delivery": "2025-11-03",
        "total": "$89.99"
    },
    "ORD123457": {
        "status": "Processing",
        "items": ["Laptop Stand", "USB Cable"],
        "tracking": None,
        "estimated_delivery": "2025-11-05",
        "total": "$45.50"
    },
    "ORD123458": {
        "status": "Delivered",
        "items": ["Coffee Mug", "Notebook"],
        "tracking": "1Z999AA1234567891",
        "estimated_delivery": "2025-10-30",
        "total": "$24.99"
    },
    "ORD123459": {
        "status": "Cancelled",
        "items": ["Smartwatch"],
        "tracking": None,
        "estimated_delivery": None,
        "total": "$299.99"
    }
}

# Product Catalog
PRODUCT_CATALOG = {
    "wireless_headphones": {
        "name": "Premium Wireless Headphones",
        "price": "$79.99",
        "in_stock": True,
        "stock_count": 15,
        "description": "High-quality wireless headphones with noise cancellation",
        "warranty": "1 year"
    },
    "laptop_stand": {
        "name": "Adjustable Laptop Stand",
        "price": "$39.99",
        "in_stock": True,
        "stock_count": 8,
        "description": "Ergonomic aluminum laptop stand with adjustable height",
        "warranty": "6 months"
    },
    "smartwatch": {
        "name": "Fitness Smartwatch",
        "price": "$299.99",
        "in_stock": False,
        "stock_count": 0,
        "description": "Advanced fitness tracking with heart rate monitor",
        "warranty": "2 years"
    },
    "phone_case": {
        "name": "Protective Phone Case",
        "price": "$19.99",
        "in_stock": True,
        "stock_count": 50,
        "description": "Drop-proof case with screen protection",
        "warranty": "6 months"
    }
}

# Shipping Information
SHIPPING_RATES = {
    "standard": {"cost": 4.99, "days": "5-7", "free_threshold": 50},
    "express": {"cost": 9.99, "days": "2-3", "free_threshold": None},
    "overnight": {"cost": 19.99, "days": "1", "free_threshold": None}
}

def get_customer_support_data() -> List[Dict[str, Any]]:
    """Get all customer support documents."""
    return CUSTOMER_SUPPORT_DOCS

def get_order_status(order_id: str) -> Dict[str, Any]:
    """Get order status by order ID."""
    return CUSTOMER_ORDERS_DB.get(order_id, {
        "status": "Not Found",
        "message": "Order not found. Please check your order number."
    })

def get_product_info(product_name: str) -> Dict[str, Any]:
    """Get product information by name."""
    product_key = product_name.lower().replace(" ", "_")
    return PRODUCT_CATALOG.get(product_key, {
        "name": "Product not found",
        "message": "Product not available in our catalog"
    })

def calculate_shipping(order_total: float, shipping_type: str = "standard") -> Dict[str, Any]:
    """Calculate shipping cost based on order total and shipping type."""
    if shipping_type not in SHIPPING_RATES:
        return {"error": "Invalid shipping type"}

    rate = SHIPPING_RATES[shipping_type]

    # Check if eligible for free shipping
    if rate["free_threshold"] and order_total >= rate["free_threshold"]:
        cost = 0.0
    else:
        cost = rate["cost"]

    return {
        "shipping_type": shipping_type,
        "cost": cost,
        "delivery_time": rate["days"] + " business days",
        "free_shipping_eligible": cost == 0.0
    }
