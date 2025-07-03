$(document).ready(function() {

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function sendSalonNameToServer(salonName) {
    fetch("/api/send-salon/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: JSON.stringify({ name: salonName })
    })
    .then(response => response.json())
    .then(data => {
        if (data.masters_html) {
            document.querySelector(".service__masters > .panel").innerHTML = data.masters_html;
        }
    })
    .catch(error => console.error("Ошибка при отправке:", error));
}

	$('.salonsSlider').slick({
		arrows: true,
	  slidesToShow: 4,
	  infinite: true,
	  prevArrow: $('.salons .leftArrow'),
	  nextArrow: $('.salons .rightArrow'),
	  responsive: [
	    {
	      breakpoint: 991,
	      settings: {
	        
	      	centerMode: true,
  			//centerPadding: '60px',
	        slidesToShow: 2
	      }
	    },
	    {
	      breakpoint: 575,
	      settings: {
	        slidesToShow: 1
	      }
	    }
	  ]
	});
	$('.servicesSlider').slick({
		arrows: true,
	  slidesToShow: 4,
	  prevArrow: $('.services .leftArrow'),
	  nextArrow: $('.services .rightArrow'),
	  responsive: [
	  	{
	      breakpoint: 1199,
	      settings: {
	        

	        slidesToShow: 3
	      }
	    },
	    {
	      breakpoint: 991,
	      settings: {
	        
	      	centerMode: true,
  			//centerPadding: '60px',
	        slidesToShow: 2
	      }
	    },
	    {
	      breakpoint: 575,
	      settings: {
	        slidesToShow: 1
	      }
	    }
	  ]
	});

	$('.mastersSlider').slick({
		arrows: true,
	  slidesToShow: 4,
	  prevArrow: $('.masters .leftArrow'),
	  nextArrow: $('.masters .rightArrow'),
	  responsive: [
	  	{
	      breakpoint: 1199,
	      settings: {
	        

	        slidesToShow: 3
	      }
	    },
	    {
	      breakpoint: 991,
	      settings: {
	        

	        slidesToShow: 2
	      }
	    },
	    {
	      breakpoint: 575,
	      settings: {
	        slidesToShow: 1
	      }
	    }
	  ]
	});

	$('.reviewsSlider').slick({
		arrows: true,
	  slidesToShow: 4,
	  prevArrow: $('.reviews .leftArrow'),
	  nextArrow: $('.reviews .rightArrow'),
	  responsive: [
	  	{
	      breakpoint: 1199,
	      settings: {
	        

	        slidesToShow: 3
	      }
	    },
	    {
	      breakpoint: 991,
	      settings: {
	        

	        slidesToShow: 2
	      }
	    },
	    {
	      breakpoint: 575,
	      settings: {
	        slidesToShow: 1
	      }
	    }
	  ]
	});

	// menu
	$('.header__mobMenu').click(function() {
		$('#mobMenu').show()
	})
	$('.mobMenuClose').click(function() {
		$('#mobMenu').hide()
	})

	var acc = document.getElementsByClassName("accordion");
	var i;

	for (i = 0; i < acc.length; i++) {
	  acc[i].addEventListener("click", function(e) {
	  	e.preventDefault()
	    this.classList.toggle("active");
	    var panel = $(this).next()
	    panel.hasClass('active') ?  
	    	 panel.removeClass('active')
	    	: 
	    	 panel.addClass('active')
	  });
	}


	$(document).on('click', '.accordion__block input[type="radio"]', function(e) {
		let $block = $(this).closest('.accordion__block');

		let thisName = $block.find('.accordion__block_intro').text();
    	let thisAddress = $block.find('.accordion__block_address').text()

		console.log(thisName)
		sendSalonNameToServer(thisName)

		let $accordionButton = $block.closest('.service__salons').find('> .accordion');
    	$accordionButton.addClass('selected').text(thisName + ' - ' + thisAddress);
		
		setTimeout(() => {
			$accordionButton.click();
		}, 200);
	})


	$('.accordion__block_item').click(function(e) {
		let thisName,thisAddress;
		thisName = $(this).find('> .accordion__block_item_intro').text()
		thisAddress = $(this).find('> .accordion__block_item_address').text()
		$(this).parent().parent().parent().parent().find('> button.active').addClass('selected').text(thisName + '  ' +thisAddress)

		setTimeout(() => {
			$(this).parent().parent().parent().parent().find('> button.active').click()
		}, 200)
	})


	$(document).on('click', '.service__masters .accordion__block', function(e) {
		let clone = $(this).clone()
		console.log(clone)
		$(this).parent().parent().find('> button.active').html(clone)
	})


	//popup
	$('.header__block_auth').click(function(e) {
		e.preventDefault()
		$('#authModal').arcticmodal();
		// $('#confirmModal').arcticmodal();

	})

	$('.rewiewPopupOpen').click(function(e) {
		e.preventDefault()
		$('#reviewModal').arcticmodal();
	})
	$('.payPopupOpen').click(function(e) {
		e.preventDefault()
		$('#paymentModal').arcticmodal();
	})
	$('.tipsPopupOpen').click(function(e) {
		e.preventDefault()
		$('#tipsModal').arcticmodal();
	})
	
	$('.authPopup__form').submit(function() {
		$('#confirmModal').arcticmodal();
		return false
	})

	//service
    // Инициализация datepicker
const datepickerInstance = new AirDatepicker('#datepickerHere', {
        dateFormat: 'yyyy-MM-dd',
        minDate: new Date(),
        onSelect: function({ date }) {
            updateHiddenDateField(date);
            const activeTimeBtn = $('.time__elems_btn.active');
            if (activeTimeBtn.length) {
                updateHiddenTimeField(activeTimeBtn.data('time'));
            }
        }
    });

    // Обработчик для кнопок времени
    $(document).on('click', '.time__elems_btn', function(e) {
        e.preventDefault();
        const selectedDate = datepickerInstance.selectedDates[0];
        if (!selectedDate) {
            alert('Пожалуйста, сначала выберите дату');
            return;
        }
        $('.time__elems_btn').removeClass('active');
        $(this).addClass('active');
        updateHiddenDateField(selectedDate);
        updateHiddenTimeField($(this).data('time'));
    });

    // Функции для обновления скрытых полей
    function updateHiddenDateField(date) {
        $('input[name="selected_date"]').remove();
        if (date) {
            const dateStr = formatDate(date);
            $('<input>').attr({
                type: 'hidden',
                name: 'selected_date',
                value: dateStr
            }).appendTo('.service__form');
        }
    }

    function updateHiddenTimeField(time) {
        $('input[name="selected_time"]').remove();
        if (time) {
            $('<input>').attr({
                type: 'hidden',
                name: 'selected_time',
                value: time
            }).appendTo('.service__form');
        }
    }

    // Форматирование даты
    function formatDate(date) {
        const d = new Date(date);
        const year = d.getFullYear();
        const month = String(d.getMonth() + 1).padStart(2, '0');
        const day = String(d.getDate()).padStart(2, '0');
        return `${year}-${month}-${day}`;
    }

    // Проверка перед отправкой формы
    $('.service__form').on('submit', function(e) {
        const selectedDate = datepickerInstance.selectedDates[0];
        const selectedTime = $('.time__elems_btn.active').data('time');
        if (!selectedDate || !selectedTime) {
            e.preventDefault();
            alert('Пожалуйста, выберите дату и время');
        }
    });
})