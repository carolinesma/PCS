import arithmetic_coding as ac

def show_results(symbol, code_interval, source_interval): 
    
    print(f"\nSímbolo Atual {[symbol]}")  
    print("Intervalo Candidato:")
    code_interval.print()
    print("Intervalo Fonte:")
    source_interval.print()