var content = document.getElementsByClassName("contentEdit")
let a = false;
const contentArray = []
  for (let i = 0; i < content.length;i++){
    contentArray[i] = content[i].innerHTML
  }
  // console.log(localStorage.getItem("contentEdit"))


window.addEventListener('load', (event) =>{
  console.log(content)
  content[0].innerHTML = localStorage.getItem("basic contentEdit")
  content[1].innerHTML = localStorage.getItem("mb-0 contentEdit")
  content[2].innerHTML = localStorage.getItem("contentEdit")
  content[3].innerHTML = localStorage.getItem("mb-1-9 contentEdit")
  console.log(localStorage);
});


function edit(){
  var button = document.getElementsByClassName("contentEdit")
  for (let i = 0; i < button.length;i++){
    button[i].contentEditable = "true"
  }
}

function save(){
  var content = document.getElementsByClassName("contentEdit")
  for (let i = 0; i < content.length;i++){
    content[i].contentEditable = "false"
    localStorage.setItem(content[i].getAttribute("class"), content[i].innerHTML);
  }
}

