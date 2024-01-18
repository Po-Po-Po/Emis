<template>
  <div>
    <div class="label">{{ label }}</div>
    <editor-content :editor="editor" class="editor"></editor-content>
  </div>
</template>

<script>
import {Editor, EditorContent} from '@tiptap/vue-2'
import StarterKit from '@tiptap/starter-kit'
import Link from '@tiptap/extension-link'

export default {
  components: {
    EditorContent,
  },

  props: {
    value: {
      type: String,
      default: '',
    },
    label: {
      type: String,
      default: 'Label'
    }
  },

  data() {
    return {
      editor: null,
    }
  },

  watch: {
    value(value) {
      // HTML
      const isSame = this.editor.getHTML() === value

      // JSON
      // const isSame = JSON.stringify(this.editor.getJSON()) === JSON.stringify(value)

      if (isSame) {
        return
      }

      this.editor.commands.setContent(value, false)
    },
  },

  mounted() {
    this.editor = new Editor({
      content: this.value,
      extensions: [
        StarterKit.configure({
          paragraph: {
            HTMLAttributes: {
              class: 'editor'
            }
          }
        }),
        Link
      ],
      editorProps: {
        attributes: {
          class: 'editor',
        },
        injectCSS: true,
      },
      onUpdate: () => {
        // HTML
        this.$emit('input', this.editor.getHTML())

        // JSON
        // this.$emit('input', this.editor.getJSON())
      },
    })
  },

  beforeDestroy() {
    this.editor.destroy()
  },
}
</script>
<style lang="scss">
/* Basic editor styles */
.label {
  margin-top: -11px;
  margin-left: 10px;
  position: absolute;
  z-index: 4;
  padding: 0 5px 0 5px;
  background: #fff;
}

.ProseMirror {
  border: 1px solid;
  min-height: 100px;
  width: 100%;
  border-radius: 0.25em;
  padding: 5px;

  > * + * {
    margin: 0;
    padding: 0;
  }


  p {
    font-size: 0.9rem;
    margin-top: 5px;
    padding: 10px 0 0 5px;
    color: #000;
    line-height: 0;
    letter-spacing: 0.0071428571em;
  }
}
</style>
