# Código Vulnerável


Python Script to automate the task of entering a website, and copying its tags content

Currently only for linux

## Vulnerabilidades :

#### 1 - Condição no if, efetua um break, deveria de fazer um pass

```python
 for tag in LIST_HTML_TAGS:
            
    data = driver.find_element("xpath",f"//{tag}").get_attribute("innerHTML")

    if len(data) < 0:
        break # <--
    else:
        report(action,current_date,data)
                   
```

#### 2 - Não existe validação nem cria a pasta logs para gerar o log

```python
def report(action: str,current_time: datetime, data: str):
    print("Writing Log ...")
    f = open("logs/reboopy.log", "a")
    if action == "enter":
        f.write("Entered in: " + str(current_time) + " - For more information on the process, see Geckodriver.log on parent folder \n")
    if action == "copy":
        f.write("Copy Performed in: " + str(current_time) + " - For more information on the copying process, see Geckodriver.log on parent folder \n")
        f.write(f"Content of Copy: {data} \n")
    f.close()
                   
```

#### 3 - To Do, obter credenciais


