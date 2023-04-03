import time

def display_avg_value(var_update_func):
    total_value = 0
    count = 0
    
    while True:
        value = var_update_func()
        total_value += value
        count += 1
        
        if count % 5 == 0:
            avg_value = total_value / count
            print(f"Average value: {avg_value}")
            time.sleep(1)

            
# Use this in mian.py in loop
#     def update_var():
#     # code to update variable goes here
#     return value

# display_avg_value(update_var)
