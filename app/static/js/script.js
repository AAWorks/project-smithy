var content = document.getElementsByClassName("contentEdit")
const contentArray = []
  for (let i = 0; i < content.length;i++){
    contentArray[i] = content[i].innerHTML
    if (typeof(Storage) !== "undefined") {
      content[i].innerHTML = localStorage.getItem("contentEdit")


    }
  }


function edit(){
  var button = document.getElementsByClassName("contentEdit")
  for (let i = 0; i < button.length;i++){
    button[i].contentEditable = "true"
  }
}

function save(){
  var content = document.getElementsByClassName("contentEdit")
  for (let i = 0; i < content.length;i++){
    if (content[i].innerHTML != contentArray[i]){
      console.log("HELLO")
      content[i].innerHTML = content[i].innerHTML
      console.log(content[i].getAttribute("class"))
      localStorage.setItem(content[i].getAttribute("class"), content[i].innerHTML);
    }
  }
}
