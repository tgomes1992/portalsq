
  document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('select');

    var options = {
        
    }


    
    var instances = M.FormSelect.init(elems, options);
  });


months = 	[
  'Janeiro',
  'Fevereiro',
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
  
weekdays	 = [
  'Domingo',
  'Segunda',
  'Terça',
  'Quarta',
  'Quinta',
  'Sexta',
  'Sábado'
]


  document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.datepicker');
    
    var options = {
        "format" :	'dd/mm/yyyy' ,  

        'i18n': {
          cancel: 'Cancelar',
          clear: 'Limpar',
          done: 'OK',
          previousMonth: '‹',
          nextMonth: '›',
          months: [
            'Janeiro',
            'Fevereiro',
            'Março',
            'Abril',
            'Maio',
            'Junho',
            'Julho',
            'Agosto',
            'Setembro',
            'Outubro',
            'Novembro',
            'Dezembro'
        ],
        monthsShort: [
            'Jan',
            'Fev',
            'Mar',
            'Abr',
            'Mai',
            'Jun',
            'Jul',
            'Ago',
            'Set',
            'Out',
            'Nov',
            'Dez'
        ],
        weekdays: [
            'Domingo',
            'Segunda-feira',
            'Terça-feira',
            'Quarta-feira',
            'Quinta-feira',
            'Sexta-feira',
            'Sábado'
        ],
        weekdaysShort: [
            'Dom',
            'Seg',
            'Ter',
            'Qua',
            'Qui',
            'Sex',
            'Sáb'
        ],
        weekdaysAbbrev: ['D', 'S', 'T', 'Q', 'Q', 'S', 'S']

        }

      
      }
    var instances = M.Datepicker.init(elems, options);
  });