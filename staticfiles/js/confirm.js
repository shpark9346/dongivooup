
// 문서 준비 이벤트
// : HTML 문서가 모두 로딩되면, 실행되는 함수
$(function() {

    $('.num').on('click',function() {

        let num = $(this).text()

        let inputNumbers = $('input.confirm-input')

        // 앞쪽의 입력칸이 값이 들어가 있으면, 
        // 다음 칸으로 이동
        let i = 0
        for (i = 0; i < 5; i++) {
            let input = $( inputNumbers[i] ).val()
            if( input == undefined || input == '' ) {
                break
            }
        }
        
        $(inputNumbers[i]).val(num)

        if( i == 4 ) {
            // 인증번호와 입력번호가 같은지 확인
            let confirmNum = $('#confirm-num').text()
            let inputNum = ''

            for (let j = 0; j < 5; j++) {
                let input = $( inputNumbers[j] ).val()
                inputNum += input
            }

            // console.log('confirmNum : ' + confirmNum);
            // console.log('inputNum : ' + inputNum);

            // 일치하는지 확인
            if( confirmNum == inputNum ) {
                alert('일치')
            } else {
                alert('불일치')
            }
        }


        // 5칸 다 입력시, 또 입력
        if( i == 5 ) {
            alert('이미 모든 칸이 입력되었습니다.')
            console.log('이미 모든 칸이 입력되었습니다.');
        }


        $('#reload').on('click', function(){
            $('.confirm-input').val('')
        })


    })



})