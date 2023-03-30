/ Add $ and checksum to result
/ pass parameters as Integers

def generate_thd_sentence(forward_thrust):
    sentence = f'CCTHD,{forward_thrust.2f},0.00,0.00,0.00,0.00,0.00,0.00,0.00'
    return sentence
  
def generate_hsc_sentence(heading):
    sentence = f'CCHSC,{heading:.1f},T,,'
    return sentence
  
  /The T after the heading value represents the reference direction, in this case, True North. 
  /The two empty commas at the end of the sentence are placeholders for the magnetic 
  /heading and the magnetic variation, respectively, which are not included
