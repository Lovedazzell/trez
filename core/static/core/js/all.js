



// to open the menu bar
function sidebar(){
    let ele = document.getElementById('sidebar');
    ele.style.visibility = 'visible';
  };


  // to close the ment bar
  const sidebarclose =()=>{
    let ele = document.getElementById('sidebar');
    ele.style.visibility = 'hidden';
  }

// to lower the bit value
  const minus = ()=>{
   
    let m = document.getElementById('number').value
    let value = parseInt(m)
    if(value <= 1 ){
      document.getElementById('error').style.display = 'block'
      
    }else{
    
      let new_value =  value -=  1
   
      document.getElementById('number').value = new_value
   
      document.getElementById('total').innerHTML =  10*parseInt(new_value)


    }
  }



  

  // to inerease the bit value
  const increment = ()=>{
   
    let m = document.getElementById('number').value
    let value = parseInt(m)
    document.getElementById('error').style.display = 'none'
    let new_value =  value +=  1
    document.getElementById('number').value = new_value

    document.getElementById('total').innerHTML =  10*parseInt(new_value)

    
  };

// Change the total gems value after changing the input value
  $('#number').keyup(function(){
    let t_d = document.getElementById('total').innerHTML 
    let new_d = document.getElementById('number').value
    if(document.getElementById('number').value >= 1){

      document.getElementById('total').innerHTML  = 10*parseInt(new_d )
      document.getElementById('error').style.display = 'none'
    }else{
    document.getElementById('error').style.display = 'block'
    }

    
      });


// to close the module
const closeModal=()=>{
    document.getElementById('money-modal-parent').style.visibility = 'hidden'
};