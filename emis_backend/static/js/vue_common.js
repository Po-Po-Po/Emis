window.url_in_text = new Vue({
    el: '#url_in_text',
    components: {},
    data: () => ({
        text: window.text,
        text_html: '',
        editText: false
    }),
    delimiters: ['[[', ']]'],
    mounted(){
        this.text_html = this.urlify(this.text)
    },
    methods: {
        urlify(text) {
          let urlRegex = /(https?:\/\/[^\s]+)/g;
          return text.replace(urlRegex, function(url) {
            return '<a href="' + url + '" target="_blank">' + url + '</a>';
          })
        }
    }
})