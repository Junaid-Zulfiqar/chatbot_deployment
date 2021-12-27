class Chatbox {
    constructor () {
        this.args = {
            openButton: document.querySelector('.chatbox__button'),
            chatBox: document.querySelector('.chatbox__support'),
            sendButton: document.querySelector('.send__button')
        }

        this.state = false;
        this.messages = [];
    }

    display() {
        const {openButton, chatBox, sendButton} = this.args;

        openButton.addEventListener('click' , () => this.toggleState(chatbox))
        sendButton.addEventListener('click' , () => this.onsendButton(chatbox))

        const node = chatBox.querySelector('input');
        node.addEventListener("keyup", ({key}) => {
            if (key === "Enter") {
                this.onsendButton(chatBox)
            }
        })
    }    

    toggleState(chatbox) {

        this.state = !this.state;

        if(this.state) {
            document.querySelector('.chatbox__support').classList.add('chatbox--active')
        } else {
            document.querySelector('.chatbox__support').classList.remove(tokens='chatbox--active')
        }
    }

    onsendButton(chatbox) {
        var textField = document.querySelector('.chatbox__support').querySelector('input');
        let text1 = textField.value
        if (text1 === "") {
            return;
        }
        let msg1 = { name: "User", message:text1}
        this.messages.push(msg1)


        // 'http://127.0.0.1:8000/predict
        fetch("http://localhost:8000/predict",{
            method: 'POST',
            body: JSON.stringify({value:{message:text1}}),
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json'
            },
        })
        .then(r => r.json())
        .then(r => {
            console.log("Check");
            let msg2 = { name: "matebot", message: r.answer, time : r.msg_time};
            this.messages.push(msg2);
            this.updateChatText(chatbox)
            textField.value = ''

        }).catch((error) => {
            console.error('Error:', error);
            // this.updateChatText(chatbox)
            textField.value = ''
        });
    }

    updateChatText(chatbox) {
        console.log(this.messages);
        var html = '';
        this.messages.reverse().forEach(function(item, index) {
            if (item.name === 'matebot'){
                html += '<div class="messages__item messages__item--visitor">' + item.message +  '<br/><small>' + item.time + '</small></div>'
            }
            else {
                html += '<div class="messages__item messages__item--operator">' + item.message +  '<br/><small>' + new Date ().toLocaleTimeString() + '</small></div>'
            }
        });
        

        // const chatmessage = document.querySelector('.chatbox__support').querySelector('.chatbox__messages');
        const chatmessage = document.querySelector(".chatbox__support").querySelector('.chatbox__messages');
        chatmessage.innerHTML = html;
    }
}

const chatbox = new Chatbox();
chatbox.display();


