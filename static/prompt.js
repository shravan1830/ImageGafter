const LOCALHOST = "http://127.0.0.1:5000"
const progress_bar = document.getElementById("progress_bar")
const container = document.getElementsByClassName("container")[0]
const populate_cards = async (data) =>
    {
        let card = document.getElementsByClassName('swiper-slide')[0]

        const data_len = Object.keys(data).length 
        for(let idx = 1; idx < data_len ; idx++)
        {
            const new_card = card.cloneNode(true)
            card.after(new_card)
            card = new_card
        }
        let idx = 0
        for (const img_file in data) {

            const card_img = document.getElementsByClassName("card-img-top")[idx]
            const card_txt = document.getElementsByClassName("card-text")[idx]
            card_img.src = `${LOCALHOST}/get_image/${img_file}`
            card_txt.textContent = data[img_file]
            idx++

        }
    }


const get_prompts =  async () =>
    {
        
        const res =  await fetch(`${LOCALHOST}/get_prompts`)
        const data = await res.json()
        progress_bar.style.display ="none"
        container.style.display = "block"
        await populate_cards(data)
    
    }
window.addEventListener("load",get_prompts)

const progress_text = document.getElementById("progress_text")
const load_txts = ["Poeticizing your pictures","Stanza crafting your shots","Visualizing your verses","Rendering your reflections"]

setInterval((e) => {
    let idx = Math.floor(Math.random() * load_txts.length)
    progress_text.textContent = load_txts[idx]
},5000)


