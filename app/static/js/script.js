function edit(){
  var button = document.getElementsByClassName("contentEdit")
  for (let i = 0; i < button.length;i++){
    button[i].contentEditable = "true"
  }
//  for (let i =1;i< 7;i++){
//   var button = document.getElementById("contentEdit" + String(i))
//   console.log("contentEdit" + String(i))
//   button.contentEditable = "true"
//  }
// window.onclick = e => {
//   if(e.target.tagName == "INPUT"){
//     console.log(e.target.parentElement)
//     e.target.parentElement.contentEditable = "true"
//   }
}

function save(){


}