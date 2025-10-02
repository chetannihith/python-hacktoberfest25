import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from typing import List, Optional

# Factory Pattern - MenuItem Factory
class MenuItem:
    """
    Represents a menu item in the food delivery system.
    """
    def __init__(self, item_id: int, name: str, price: float, category: str):
        """
        Initializes a MenuItem instance.

        :param item_id: Unique identifier for the item.
        :param name: Name of the menu item.
        :param price: Price of the item.
        :param category: Category of the item (e.g., 'Main', 'Side').
        """
        self.item_id = item_id
        self.name = name
        self.price = price
        self.category = category
    
    def __str__(self) -> str:
        """
        Returns a string representation of the menu item.
        """
        return f"{self.name} - ${self.price:.2f}"

class MenuItemFactory:
    """
    Factory class for creating MenuItem instances.
    """
    @staticmethod
    def create_menu_item(item_type: str) -> Optional[MenuItem]:
        """
        Creates a MenuItem based on the given type.

        :param item_type: Type of the menu item (e.g., 'pizza', 'burger').
        :return: MenuItem instance or None if type is invalid.
        """
        items = {
            'pizza': MenuItem(1, 'Pizza', 12.99, 'Main'),
            'burger': MenuItem(2, 'Burger', 8.99, 'Main'),
            'salad': MenuItem(3, 'Salad', 6.99, 'Side'),
            'drink': MenuItem(4, 'Drink', 2.99, 'Beverage')
        }
        return items.get(item_type)
    
    @staticmethod
    def get_all_menu_items() -> List[MenuItem]:
        """
        Returns a list of all available menu items.
        """
        return [MenuItemFactory.create_menu_item(t) for t in ['pizza', 'burger', 'salad', 'drink']]

# Factory Pattern - User Factory
class User:
    """
    Represents a user with a specific role in the system.
    """
    def __init__(self, role: str):
        """
        Initializes a User instance.

        :param role: Role of the user (e.g., 'customer', 'restaurant').
        """
        self.role = role
    
    def can_place_order(self) -> bool:
        """
        Checks if the user can place orders.
        """
        return self.role == 'customer'
    
    def can_prepare_order(self) -> bool:
        """
        Checks if the user can prepare orders.
        """
        return self.role == 'restaurant'
    
    def can_deliver_order(self) -> bool:
        """
        Checks if the user can deliver orders.
        """
        return self.role == 'delivery'
    
    def can_cancel_order(self) -> bool:
        """
        Checks if the user can cancel orders.
        """
        return self.role == 'admin'

class UserFactory:
    """
    Factory class for creating User instances.
    """
    @staticmethod
    def create_user(role: str) -> User:
        """
        Creates a User with the specified role.

        :param role: Role for the new user.
        :return: User instance.
        """
        return User(role)

# Order Management
class Order:
    """
    Represents an order in the food delivery system.
    """
    order_counter = 1
    
    def __init__(self, items: List[MenuItem]):
        """
        Initializes an Order instance.

        :param items: List of MenuItem instances in the order.
        """
        self.order_id = Order.order_counter
        Order.order_counter += 1
        self.items = items
        self.status = 'Placed'
        self.timestamp = datetime.now().strftime("%H:%M:%S")
    
    def get_total(self) -> float:
        """
        Calculates the total price of the order.
        """
        return sum(item.price for item in self.items)
    
    def update_status(self, new_status: str) -> None:
        """
        Updates the status of the order.

        :param new_status: New status for the order.
        """
        self.status = new_status

# Main Application
class FoodDeliveryApp:
    """
    Main application class for the Food Delivery System GUI.
    """
    def __init__(self, root: tk.Tk):
        """
        Initializes the FoodDeliveryApp.

        :param root: The root Tkinter window.
        """
        self.root = root
        self.root.title("Food Delivery System")
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f0f0')
        
        self.current_user = UserFactory.create_user('customer')
        self.cart: List[MenuItem] = []
        self.orders: List[Order] = []
        self.events: List[str] = []
        
        self.style = ttk.Style()
        self.style.configure('TButton', font=('Arial', 9, 'bold'), padding=5)
        self.style.configure('TRadiobutton', font=('Arial', 10), background='white')
        
        self.setup_ui()
        self.log_event("Application started")
    
    def setup_ui(self) -> None:
        """
        Sets up the user interface components.
        """
        # Header
        header_frame = tk.Frame(self.root, bg='#2c3e50', height=60)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="🍕 Food Delivery App", 
                               font=('Arial', 20, 'bold'), bg='#2c3e50', fg='white')
        title_label.pack(pady=15)
        
        # Main container
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Left Panel - Role and Menu
        left_frame = tk.Frame(main_frame, bg='white', relief='raised', bd=2)
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))
        
        # Role Selection
        role_frame = ttk.LabelFrame(left_frame, text="Select Role", 
                                    padding=10)
        role_frame.pack(fill='x', padx=10, pady=10)
        
        self.role_var = tk.StringVar(value='customer')
        roles = [('👤 Customer', 'customer'), ('🍳 Restaurant', 'restaurant'), 
                 ('🚚 Delivery Partner', 'delivery'), ('👨‍💼 Admin', 'admin')]
        
        for text, role in roles:
            rb = ttk.Radiobutton(role_frame, text=text, variable=self.role_var, value=role,
                                 command=self.change_role)
            rb.pack(anchor='w', pady=2)
        
        # Menu Section
        menu_frame = ttk.LabelFrame(left_frame, text="Menu", 
                                    padding=10)
        menu_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        menu_items = MenuItemFactory.get_all_menu_items()
        for item in menu_items:
            item_frame = tk.Frame(menu_frame, bg='#ecf0f1', relief='raised', bd=1)
            item_frame.pack(fill='x', pady=5)
            
            info_label = tk.Label(item_frame, text=str(item), font=('Arial', 10),
                                  bg='#ecf0f1', anchor='w')
            info_label.pack(side='left', padx=10, pady=8)
            
            add_btn = ttk.Button(item_frame, text="Add to Cart", command=lambda i=item: self.add_to_cart(i),
                                 style='TButton')
            add_btn.pack(side='right', padx=10, pady=5)
        
        # Right Panel - Cart and Orders
        right_frame = tk.Frame(main_frame, bg='white', relief='raised', bd=2)
        right_frame.pack(side='right', fill='both', expand=True, padx=(5, 0))
        
        # Cart Section
        cart_frame = ttk.LabelFrame(right_frame, text="🛒 Shopping Cart", 
                                    padding=10)
        cart_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        cart_scroll_frame = tk.Frame(cart_frame, bg='white')
        cart_scroll_frame.pack(fill='both', expand=True)
        
        cart_scrollbar = ttk.Scrollbar(cart_scroll_frame)
        cart_scrollbar.pack(side='right', fill='y')
        
        self.cart_listbox = tk.Listbox(cart_scroll_frame, yscrollcommand=cart_scrollbar.set,
                                       font=('Arial', 10), bg='#f8f9fa', relief='flat',
                                       selectmode='single', height=8)
        self.cart_listbox.pack(side='left', fill='both', expand=True)
        cart_scrollbar.configure(command=self.cart_listbox.yview)
        
        cart_btn_frame = tk.Frame(cart_frame, bg='white')
        cart_btn_frame.pack(fill='x', pady=5)
        
        remove_btn = ttk.Button(cart_btn_frame, text="Remove Item", command=self.remove_from_cart,
                                style='TButton')
        remove_btn.pack(side='left', padx=5)
        
        clear_btn = ttk.Button(cart_btn_frame, text="Clear Cart", command=self.clear_cart,
                               style='TButton')
        clear_btn.pack(side='left', padx=5)
        
        self.total_label = tk.Label(cart_frame, text="Total: $0.00", font=('Arial', 11, 'bold'),
                                    bg='white', fg='#27ae60')
        self.total_label.pack(pady=5)
        
        place_order_btn = ttk.Button(cart_frame, text="Place Order", command=self.place_order,
                                     style='TButton')
        place_order_btn.pack(pady=5)
        
        # Orders Section
        orders_frame = ttk.LabelFrame(right_frame, text="📦 Orders", 
                                      padding=10)
        orders_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        orders_scroll_frame = tk.Frame(orders_frame, bg='white')
        orders_scroll_frame.pack(fill='both', expand=True)
        
        orders_scrollbar = ttk.Scrollbar(orders_scroll_frame)
        orders_scrollbar.pack(side='right', fill='y')
        
        self.orders_listbox = tk.Listbox(orders_scroll_frame, yscrollcommand=orders_scrollbar.set,
                                         font=('Arial', 9), bg='#f8f9fa', relief='flat',
                                         selectmode='single', height=6)
        self.orders_listbox.pack(side='left', fill='both', expand=True)
        orders_scrollbar.configure(command=self.orders_listbox.yview)
        
        order_btn_frame = tk.Frame(orders_frame, bg='white')
        order_btn_frame.pack(fill='x', pady=5)
        
        self.prepare_btn = ttk.Button(order_btn_frame, text="Prepare Order", 
                                      command=self.prepare_order, style='TButton')
        self.prepare_btn.pack(side='left', padx=2)
        
        self.pickup_btn = ttk.Button(order_btn_frame, text="Pick Up", 
                                     command=self.pickup_order, style='TButton')
        self.pickup_btn.pack(side='left', padx=2)
        
        self.deliver_btn = ttk.Button(order_btn_frame, text="Deliver", 
                                      command=self.deliver_order, style='TButton')
        self.deliver_btn.pack(side='left', padx=2)
        
        self.cancel_btn = ttk.Button(order_btn_frame, text="Cancel", 
                                     command=self.cancel_order, style='TButton')
        self.cancel_btn.pack(side='left', padx=2)
        
        # Event Log
        log_frame = ttk.LabelFrame(self.root, text="📋 Activity Log", 
                                   padding=10)
        log_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        log_scroll_frame = tk.Frame(log_frame, bg='white')
        log_scroll_frame.pack(fill='both', expand=True)
        
        log_scrollbar = ttk.Scrollbar(log_scroll_frame)
        log_scrollbar.pack(side='right', fill='y')
        
        self.log_text = tk.Text(log_scroll_frame, height=6, yscrollcommand=log_scrollbar.set,
                                font=('Courier', 9), bg='#2c3e50', fg='#ecf0f1',
                                relief='flat', wrap='word')
        self.log_text.pack(side='left', fill='both', expand=True)
        log_scrollbar.configure(command=self.log_text.yview)
        self.log_text.configure(state='disabled')
        
        self.update_ui_state()
    
    def change_role(self) -> None:
        """
        Changes the current user's role and updates the UI.
        """
        role = self.role_var.get()
        self.current_user = UserFactory.create_user(role)
        role_names = {'customer': 'Customer', 'restaurant': 'Restaurant', 
                      'delivery': 'Delivery Partner', 'admin': 'Admin'}
        self.log_event(f"Switched to {role_names[role]} role")
        self.update_ui_state()
    
    def update_ui_state(self) -> None:
        """
        Updates the state of UI buttons based on the current user's role.
        """
        can_place = self.current_user.can_place_order()
        can_prepare = self.current_user.can_prepare_order()
        can_deliver = self.current_user.can_deliver_order()
        can_cancel = self.current_user.can_cancel_order()
        
        state_prepare = 'normal' if can_prepare else 'disabled'
        state_pickup = 'normal' if can_deliver else 'disabled'
        state_deliver = 'normal' if can_deliver else 'disabled'
        state_cancel = 'normal' if can_cancel else 'disabled'
        
        self.prepare_btn.configure(state=state_prepare)
        self.pickup_btn.configure(state=state_pickup)
        self.deliver_btn.configure(state=state_deliver)
        self.cancel_btn.configure(state=state_cancel)
    
    def add_to_cart(self, item: MenuItem) -> None:
        """
        Adds an item to the shopping cart if allowed.

        :param item: MenuItem to add.
        """
        if not self.current_user.can_place_order():
            messagebox.showwarning("Access Denied", "Only customers can add items to cart!")
            return
        
        self.cart.append(item)
        self.update_cart_display()
        self.log_event(f"Added {item.name} to cart")
    
    def remove_from_cart(self) -> None:
        """
        Removes the selected item from the cart.
        """
        selection = self.cart_listbox.curselection()
        if selection:
            index = selection[0]
            item = self.cart[index]
            self.cart.pop(index)
            self.update_cart_display()
            self.log_event(f"Removed {item.name} from cart")
    
    def clear_cart(self) -> None:
        """
        Clears all items from the cart.
        """
        if self.cart:
            self.cart.clear()
            self.update_cart_display()
            self.log_event("Cart cleared")
    
    def update_cart_display(self) -> None:
        """
        Updates the cart listbox display and total label.
        """
        self.cart_listbox.delete(0, tk.END)
        total = 0.0
        for item in self.cart:
            self.cart_listbox.insert(tk.END, f"{item.name} - ${item.price:.2f}")
            total += item.price
        self.total_label.configure(text=f"Total: ${total:.2f}")
    
    def place_order(self) -> None:
        """
        Places an order with the current cart items if allowed.
        """
        if not self.current_user.can_place_order():
            messagebox.showwarning("Access Denied", "Only customers can place orders!")
            return
        
        if not self.cart:
            messagebox.showwarning("Empty Cart", "Please add items to cart first!")
            return
        
        order = Order(self.cart.copy())
        self.orders.append(order)
        self.log_event(f"Order #{order.order_id} placed - Total: ${order.get_total():.2f}")
        self.cart.clear()
        self.update_cart_display()
        self.update_orders_display()
        messagebox.showinfo("Success", f"Order #{order.order_id} placed successfully!")
    
    def prepare_order(self) -> None:
        """
        Prepares the selected order if allowed.
        """
        if not self.current_user.can_prepare_order():
            messagebox.showwarning("Access Denied", "Only restaurant staff can prepare orders!")
            return
        
        selection = self.orders_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select an order to prepare!")
            return
        
        order = self.orders[selection[0]]
        if order.status != 'Placed':
            messagebox.showwarning("Invalid Action", f"Order is already {order.status}!")
            return
        
        order.update_status('Prepared')
        self.update_orders_display()
        self.log_event(f"Order #{order.order_id} prepared by restaurant")
    
    def pickup_order(self) -> None:
        """
        Marks the selected order as picked up for delivery if allowed.
        """
        if not self.current_user.can_deliver_order():
            messagebox.showwarning("Access Denied", "Only delivery partners can pick up orders!")
            return
        
        selection = self.orders_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select an order to pick up!")
            return
        
        order = self.orders[selection[0]]
        if order.status != 'Prepared':
            messagebox.showwarning("Invalid Action", "Order must be prepared first!")
            return
        
        order.update_status('Out for Delivery')
        self.update_orders_display()
        self.log_event(f"Order #{order.order_id} picked up for delivery")
    
    def deliver_order(self) -> None:
        """
        Marks the selected order as delivered if allowed.
        """
        if not self.current_user.can_deliver_order():
            messagebox.showwarning("Access Denied", "Only delivery partners can deliver orders!")
            return
        
        selection = self.orders_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select an order to deliver!")
            return
        
        order = self.orders[selection[0]]
        if order.status != 'Out for Delivery':
            messagebox.showwarning("Invalid Action", "Order must be out for delivery first!")
            return
        
        order.update_status('Delivered')
        self.update_orders_display()
        self.log_event(f"Order #{order.order_id} delivered successfully")
        messagebox.showinfo("Success", f"Order #{order.order_id} delivered!")
    
    def cancel_order(self) -> None:
        """
        Cancels the selected order if allowed.
        """
        if not self.current_user.can_cancel_order():
            messagebox.showwarning("Access Denied", "Only admins can cancel orders!")
            return
        
        selection = self.orders_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select an order to cancel!")
            return
        
        order = self.orders[selection[0]]
        if order.status == 'Delivered':
            messagebox.showwarning("Invalid Action", "Cannot cancel delivered orders!")
            return
        
        order.update_status('Cancelled')
        self.update_orders_display()
        self.log_event(f"Order #{order.order_id} cancelled by admin")
    
    def update_orders_display(self) -> None:
        """
        Updates the orders listbox display.
        """
        self.orders_listbox.delete(0, tk.END)
        status_emoji = {'Placed': '📝', 'Prepared': '🍳', 'Out for Delivery': '🚚', 
                        'Delivered': '✅', 'Cancelled': '❌'}
        for order in self.orders:
            emoji = status_emoji.get(order.status, '📦')
            self.orders_listbox.insert(tk.END, 
                                       f"{emoji} Order #{order.order_id} - {order.status} - ${order.get_total():.2f}")
    
    def log_event(self, message: str) -> None:
        """
        Logs an event to the activity log.

        :param message: Message to log.
        """
        timestamp = datetime.now().strftime("%H:%M:%S")
        event = f"[{timestamp}] {message}"
        self.events.append(event)
        self.log_text.configure(state='normal')
        self.log_text.insert(tk.END, event + "\n")
        self.log_text.see(tk.END)
        self.log_text.configure(state='disabled')

# Run Application
if __name__ == "__main__":
    root = tk.Tk()
    app = FoodDeliveryApp(root)
    root.mainloop()