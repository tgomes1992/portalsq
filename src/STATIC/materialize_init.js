
  document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('select');

    var options = {
        
    }


    
    var instances = M.FormSelect.init(elems, options);
  });


months = 	[
  'January',
  'February',
  'March',
  'April',
  'May',
  'June',
  'July',
  'August',
  'September',
  'October',
  'November',
  'December'
]
  

  document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.datepicker');
    
    var options = {
        "format" :	'dd/mm/yyyy' ,  
        "monthsShort": [ 'Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez' ],
       "monthsFull": [ 'Janeiro', 'Fevereiro', 'Marco', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro' ]
      }
    var instances = M.Datepicker.init(elems, options);
  });