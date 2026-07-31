"""
python src/demo.py
"""
from policy_engine import authorize

principal = "alice"
action = "DeleteCustomer"
resource = "Customer123"

print("=== Authorization Request ===")
print(f"Principal : {principal}")
print(f"Action    : {action}")
print(f"Resource  : {resource}")

allowed = authorize(principal, action, resource)

print()

if allowed:
    print("Decision  : ALLOW")
    print("Customer deleted.")
else:
    print("Decision  : DENY")
    print("Access denied.")
