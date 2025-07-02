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


	$(document).on('click', '.accordion__block', function(e) {
		let thisName,thisAddress;

		thisName = $(this).find('> .accordion__block_intro').text()
		thisAddress = $(this).find('> .accordion__block_address').text()
		
		
//		if(thisName === 'BeautyCity Пушкинская') {
//			$('.service__masters > .panel').html(`
//				<div class="accordion__block fic">
//						  	<div class="accordion__block_elems fic">
//							  	<img src="img/masters/avatar/all.svg" alt="avatar" class="accordion__block_img">
//							  	<div class="accordion__block_master">Любой мастер</div>
//						  	</div>
//						  </div>
//						  <div class="accordion__block fic">
//						  	<div class="accordion__block_elems fic">
//							  	<img src="img/masters/avatar/pushkinskaya/1.svg" alt="avatar" class="accordion__block_img">
//							  	<div class="accordion__block_master">Елизавета Лапина</div>
//						  	</div>
//						  	<div class="accordion__block_prof">Мастер маникюра</div>
//						  </div>
//						  <div class="accordion__block fic">
//						  	<div class="accordion__block_elems fic">
//							  	<img src="img/masters/avatar/pushkinskaya/2.svg" alt="avatar" class="accordion__block_img">
//							  	<div class="accordion__block_master">Анна Сергеева</div>
//						  	</div>
//						  	<div class="accordion__block_prof">Парикмахер</div>
//						  </div>
//						  <div class="accordion__block fic">
//						  	<div class="accordion__block_elems fic">
//							  	<img src="img/masters/avatar/pushkinskaya/3.svg" alt="avatar" class="accordion__block_img">
//							  	<div class="accordion__block_master">Ева Колесова</div>
//						  	</div>
//						  	<div class="accordion__block_prof">Визажист</div>
//						  </div>
//						  <div class="accordion__block fic">
//						  	<div class="accordion__block_elems fic">
//							  	<img src="img/masters/avatar/pushkinskaya/4.svg" alt="avatar" class="accordion__block_img">
//							  	<div class="accordion__block_master">Мария Суворова</div>
//						  	</div>
//						  	<div class="accordion__block_prof">Стилист</div>
//						  </div>
//						  <div class="accordion__block fic">
//						  	<div class="accordion__block_elems fic">
//							  	<img src="img/masters/avatar/pushkinskaya/5.svg" alt="avatar" class="accordion__block_img">
//							  	<div class="accordion__block_master">Мария Максимова</div>
//						  	</div>
//						  	<div class="accordion__block_prof">Визажист</div>
//						  </div>
//						  <div class="accordion__block fic">
//						  	<div class="accordion__block_elems fic">
//							  	<img src="img/masters/avatar/pushkinskaya/6.svg" alt="avatar" class="accordion__block_img">
//							  	<div class="accordion__block_master">Анастасия Сергеева</div>
//						  	</div>
//						  	<div class="accordion__block_prof">Визажист</div>
//						  </div>
//			`)
//			// $('.service__masters div[data-masters="Pushkinskaya"]').addClass('vib')
//		}
		console.log(thisName)
		sendSalonNameToServer(thisName)

//		if(thisName === 'BeautyCity Ленина') {
//
//			$('.service__masters > .panel').html(`
//				<div class="accordion__block fic">
//						  	<div class="accordion__block_elems fic">
//							  	<img src="img/masters/avatar/all.svg" alt="avatar" class="accordion__block_img">
//							  	<div class="accordion__block_master">Любой мастер</div>
//						  	</div>
//						  </div>
//						  <div class="accordion__block fic">
//						  	<div class="accordion__block_elems fic">
//							  	<img src="img/masters/avatar/lenina/1.svg" alt="avatar" class="accordion__block_img">
//							  	<div class="accordion__block_master">Дарья Мартынова</div>
//						  	</div>
//						  	<div class="accordion__block_prof">Мастер маникюра</div>
//						  </div>
//						  <div class="accordion__block fic">
//						  	<div class="accordion__block_elems fic">
//							  	<img src="img/masters/avatar/lenina/2.svg" alt="avatar" class="accordion__block_img">
//							  	<div class="accordion__block_master">Амина Абрамова</div>
//						  	</div>
//						  	<div class="accordion__block_prof">Парикмахер</div>
//						  </div>
//						  <div class="accordion__block fic">
//						  	<div class="accordion__block_elems fic">
//							  	<img src="img/masters/avatar/lenina/3.svg" alt="avatar" class="accordion__block_img">
//							  	<div class="accordion__block_master">Милана Романова</div>
//						  	</div>
//						  	<div class="accordion__block_prof">Визажист</div>
//						  </div>
//						  <div class="accordion__block fic">
//						  	<div class="accordion__block_elems fic">
//							  	<img src="img/masters/avatar/lenina/4.svg" alt="avatar" class="accordion__block_img">
//							  	<div class="accordion__block_master">Диана Чернова</div>
//						  	</div>
//						  	<div class="accordion__block_prof">Стилист</div>
//						  </div>
//						  <div class="accordion__block fic">
//						  	<div class="accordion__block_elems fic">
//							  	<img src="img/masters/avatar/lenina/5.svg" alt="avatar" class="accordion__block_img">
//							  	<div class="accordion__block_master">Полина Лукьянова</div>
//						  	</div>
//						  	<div class="accordion__block_prof">Визажист</div>
//						  </div>
//						  <div class="accordion__block fic">
//						  	<div class="accordion__block_elems fic">
//							  	<img src="img/masters/avatar/lenina/6.svg" alt="avatar" class="accordion__block_img">
//							  	<div class="accordion__block_master">Вера Дмитриева</div>
//						  	</div>
//						  	<div class="accordion__block_prof">Визажист</div>
//						  </div>
//			`)
//		}
//
//		if(thisName === 'BeautyCity Красная') {
//			$('.service__masters > .panel').html(`
//				<div class="accordion__block fic">
//						  	<div class="accordion__block_elems fic">
//							  	<img src="img/masters/avatar/all.svg" alt="avatar" class="accordion__block_img">
//							  	<div class="accordion__block_master">Любой мастер</div>
//						  	</div>
//						  </div>
//						  <div class="accordion__block fic">
//						  	<div class="accordion__block_elems fic">
//							  	<img src="img/masters/avatar/krasnaya/1.svg" alt="avatar" class="accordion__block_img">
//							  	<div class="accordion__block_master">Зоя Матвеева</div>
//						  	</div>
//						  </div>
//						  <div class="accordion__block fic">
//						  	<div class="accordion__block_elems fic">
//							  	<img src="img/masters/avatar/krasnaya/2.svg" alt="avatar" class="accordion__block_img">
//							  	<div class="accordion__block_master">Мария Родина</div>
//						  	</div>
//						  	<div class="accordion__block_prof">Мастер маникюра</div>
//						  </div>
//						  <div class="accordion__block fic">
//						  	<div class="accordion__block_elems fic">
//							  	<img src="img/masters/avatar/krasnaya/3.svg" alt="avatar" class="accordion__block_img">
//							  	<div class="accordion__block_master">Дарья Попова</div>
//						  	</div>
//						  	<div class="accordion__block_prof">Парикмахер</div>
//						  </div>
//						  <div class="accordion__block fic">
//						  	<div class="accordion__block_elems fic">
//							  	<img src="img/masters/avatar/krasnaya/4.svg" alt="avatar" class="accordion__block_img">
//							  	<div class="accordion__block_master">Ева Семенова</div>
//						  	</div>
//						  	<div class="accordion__block_prof">Визажист</div>
//						  </div>
//						  <div class="accordion__block fic">
//						  	<div class="accordion__block_elems fic">
//							  	<img src="img/masters/avatar/krasnaya/5.svg" alt="avatar" class="accordion__block_img">
//							  	<div class="accordion__block_master">Вера Романова</div>
//						  	</div>
//						  	<div class="accordion__block_prof">Стилист</div>
//						  </div>
//						  <div class="accordion__block fic">
//						  	<div class="accordion__block_elems fic">
//							  	<img src="img/masters/avatar/krasnaya/6.svg" alt="avatar" class="accordion__block_img">
//							  	<div class="accordion__block_master">Валерия Зуева</div>
//						  	</div>
//						  	<div class="accordion__block_prof">Визажист</div>
//						  </div>
//			`)
//
//		}

		$(this).parent().parent().find('> button.active').addClass('selected').text(thisName + '  ' +thisAddress)
		setTimeout(() => {
			$(this).parent().parent().find('> button.active').click()
		}, 200)
		
		// $(this).parent().addClass('hide')

		// console.log($(this).parent().parent().find('.panel').hasClass('selected'))
		
		// $(this).parent().parent().find('.panel').addClass('selected')
	})


	$('.accordion__block_item').click(function(e) {
		let thisName,thisAddress;
		thisName = $(this).find('> .accordion__block_item_intro').text()
		thisAddress = $(this).find('> .accordion__block_item_address').text()
		$(this).parent().parent().parent().parent().find('> button.active').addClass('selected').text(thisName + '  ' +thisAddress)
		// $(this).parent().parent().parent().parent().find('> button.active').click()
		// $(this).parent().parent().parent().addClass('hide')
		setTimeout(() => {
			$(this).parent().parent().parent().parent().find('> button.active').click()
		}, 200)
	})



	// 	console.log($('.service__masters > .panel').attr('data-masters'))
	// if($('.service__salons .accordion.selected').text() === "BeautyCity Пушкинская  ул. Пушкинская, д. 78А") {
	// }


	$(document).on('click', '.service__masters .accordion__block', function(e) {
		let clone = $(this).clone()
		console.log(clone)
		$(this).parent().parent().find('> button.active').html(clone)
	})

	// $('.accordion__block_item').click(function(e) {
	// 	const thisName = $(this).find('.accordion__block_item_intro').text()
	// 	const thisAddress = $(this).find('.accordion__block_item_address').text()
	// 	console.log($(this).parent().parent().parent().parent())
	// 	$(this).parent().parent().parent().parent().find('button.active').addClass('selected').text(thisName + '  ' +thisAddress)
	// })



	// $('.accordion__block_item').click(function(e) {
	// 	const thisChildName = $(this).text()
	// 	console.log(thisChildName)
	// 	console.log($(this).parent().parent().parent())
	// 	$(this).parent().parent().parent().parent().parent().find('button.active').addClass('selected').text(thisChildName)

	// })
	// $('.accordion.selected').click(function() {
	// 	$(this).parent().find('.panel').hasClass('selected') ? 
	// 	 $(this).parent().find('.panel').removeClass('selected')
	// 		:
	// 	$(this).parent().find('.panel').addClass('selected')
	// })


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