"""
Terminal-based Cashier Application

Features:
- Displays a menu with items and prices
- Allows selection by item number
- Prompts for quantity per selection
- Stores selections in a shopping cart
- Calculates totals and prints an itemized bill at checkout

Run: python cashier.py
"""

from dataclasses import dataclass
from typing import Dict, Tuple


@dataclass(frozen=True)
class MenuItem:
    """Represents an item that can be purchased."""

    name: str
    price: int  # stored in IDR (Rupiah)


@dataclass
class CartLine:
    """Represents a line in the shopping cart."""

    item: MenuItem
    quantity: int

    @property
    def subtotal(self) -> int:
        return self.item.price * self.quantity


def format_currency(value: int) -> str:
    """Format an integer amount as Indonesian Rupiah (e.g., Rp 25.000)."""

    return f"Rp {value:,.0f}".replace(",", ".")


def build_menu() -> Dict[int, MenuItem]:
    """Create the menu mapping numbers to items (prices in IDR)."""

    # 5 Food
    # 3 Snack
    # 2 Drink
    return {
        1: MenuItem("Nasi Goreng", 25000),   # Food
        2: MenuItem("Mie Goreng", 23000),    # Food
        3: MenuItem("Ayam Bakar", 30000),    # Food
        4: MenuItem("Sate Ayam", 28000),     # Food
        5: MenuItem("Soto Ayam", 26000),     # Food
        6: MenuItem("Pisang Goreng", 12000), # Snack
        7: MenuItem("Roti Bakar", 15000),    # Snack
        8: MenuItem("Tempe Mendoan", 10000), # Snack
        9: MenuItem("Teh Manis", 8000),      # Drink
        10: MenuItem("Kopi Tubruk", 12000),  # Drink
    }


def display_menu(menu: Dict[int, MenuItem]) -> None:
    """Print the available items and their prices."""

    print("\n=== Menu ===")
    for number, item in sorted(menu.items()):
        print(f"{number}. {item.name:<12} {format_currency(item.price)}")
    print("--------------")
    print("Enter an item number to add to cart.")
    print("Type 'c' to checkout or 'q' to quit without checkout.")


def prompt_item_selection(menu: Dict[int, MenuItem]) -> Tuple[str, int | None]:
    """Prompt for an item selection.

    Returns a tuple of (action, item_number). Action is one of:
    - 'add': item_number is a valid menu key
    - 'checkout': item_number is None
    - 'quit': item_number is None
    - 'invalid': item_number is None
    """

    user_input = input("Select item number (or 'c' to checkout, 'q' to quit): ").strip().lower()
    if user_input == "c":
        return ("checkout", None)
    if user_input == "q":
        return ("quit", None)
    if not user_input.isdigit():
        return ("invalid", None)

    item_number = int(user_input)
    if item_number not in menu:
        return ("invalid", None)
    return ("add", item_number)


def prompt_quantity() -> int | None:
    """Prompt for a positive integer quantity. Returns None if invalid."""

    qty_input = input("Enter quantity: ").strip()
    if not qty_input.isdigit():
        return None
    quantity = int(qty_input)
    if quantity <= 0:
        return None
    return quantity


def add_to_cart(cart: Dict[int, CartLine], item_number: int, menu: Dict[int, MenuItem], quantity: int) -> None:
    """Add a selected item and quantity to the cart, accumulating quantities."""

    if item_number in cart:
        cart[item_number].quantity += quantity
    else:
        cart[item_number] = CartLine(item=menu[item_number], quantity=quantity)


def calculate_total(cart: Dict[int, CartLine]) -> int:
    """Compute the total for the current cart."""

    return sum(line.subtotal for line in cart.values())


def print_receipt(cart: Dict[int, CartLine]) -> None:
    """Print an itemized receipt for the current cart."""

    if not cart:
        print("\nYour cart is empty. Nothing to checkout.")
        return

    print("\n=== Itemized Bill ===")
    print(f"{'Item':<15}{'Qty':>5}{'Price':>12}{'Subtotal':>14}")
    print("-" * 46)

    for number, line in sorted(cart.items()):
        item_name = line.item.name
        qty = line.quantity
        price_str = format_currency(line.item.price)
        subtotal_str = format_currency(line.subtotal)
        print(f"{item_name:<15}{qty:>5}{price_str:>12}{subtotal_str:>14}")

    print("-" * 46)
    total = calculate_total(cart)
    print(f"{'Total':<32}{format_currency(total):>14}")


def main() -> None:
    """Main application loop."""

    menu = build_menu()
    cart: Dict[int, CartLine] = {}

    while True:
        display_menu(menu)
        action, item_number = prompt_item_selection(menu)

        if action == "quit":
            print("\nExiting without checkout. Goodbye!")
            break

        if action == "checkout":
            print_receipt(cart)
            print("\nThank you for shopping!")
            break

        if action == "invalid":
            print("Invalid selection. Please enter a valid item number, 'c', or 'q'.")
            continue

        quantity = prompt_quantity()
        if quantity is None:
            print("Invalid quantity. Please enter a positive whole number.")
            continue

        add_to_cart(cart, item_number=item_number, menu=menu, quantity=quantity)
        selected_item = menu[item_number]
        print(
            f"Added {quantity} x {selected_item.name} to cart (Line subtotal: "
            f"{format_currency(selected_item.price * quantity)})."
        )


if __name__ == "__main__":
    main()


