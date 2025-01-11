baseName = "ds"
inputText = "*_FK"
newName = ""
if "*" in inputText:
    newName = r'''f"{baseName}{inputText.replace('*','')}"'''
    
print(eval(newName))

baseName = "dsafdsa"
print(eval(newName))