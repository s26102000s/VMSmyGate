const visitorSearchField = document.querySelector('#visitorSearchField');
const tableOutput = document.querySelector('.table-output');
const appTable = document.querySelector('.app-table');
const tbody = document.querySelector('.table-body')
tableOutput.style.display = 'none';


visitorSearchField.addEventListener('keyup', (e)=>{

   const searchval = e.target.value;
   
   if(searchval.trim().length>0){
      console.log('searchval', searchval);
      tbody.innerHTML="";
      fetch("/visitor/search-visitor", {
         body: JSON.stringify({ searchText: searchval }),
         method: "POST",
       })
         .then((res) => res.json())
         .then((data) => {
           console.log("data", data);

           appTable.style.display = 'none';
           tableOutput.style.display = 'block';

           if(data.length>0){
              data.forEach(item=>{
                tbody.innerHTML+=`
              <tr>

                <td>${item.name}</td>
                <td>${item.contact}</td>
                <td>${item.email}</td>
                <td>${item.purpose}</td>
                <td>${item.photo}</td>
                <td>${item.category}</td>
                <td>${item.date_visited}</td>
                <td>${item.host}</td>
            
              </tr>`;

              });
           }           
         });
   }else{
    appTable.style.display = 'block';
    tableOutput.style.display = 'none';
 
   }

});