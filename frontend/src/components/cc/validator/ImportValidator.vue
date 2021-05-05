<template>
  <div id="app" @dragover.prevent @drop.prevent>
    <div class="container mt-3 pt-3" @dragover="fileDragIn" @drop="handleFileDrop">

      <b-form-group label="Add your validator keys here:" label-for="input-1" label-size="m">
        <div class="file-wrapper">
          <input type="file" name="file-input" multiple="True" @change="handleFileInput" title="Put your key files here!" > Click or drag to insert key files
        </div>
      </b-form-group>

      <ul>
        <li class="key-files mt-2 pt-1" v-for="(file, index) in files" v-bind:key="file && index">
          {{ file.name }}
          <b-button variant="primary" style="height: 20px; padding:0 4px; margin-left: 5px" @click="removeFile(index)" title="delete file">delete</b-button>
        </li>
      </ul>
    </div>

    <b-form-group label="Validator password:" label-for="input-1" label-size="m">
      <input v-model="password" type="password" placeholder="min.8 characters" title="Put key file's password here!" >
    </b-form-group>

    <div class="container">
      <p class="text-center">
        <b-button variant="primary" @click="importValidator()" :disabled="files.length === 0 || password.length < 8" title="import choosen accounts">Import</b-button>
      </p>
    </div>

  </div>
</template>

<script>

export default {
  name: "ImportValidator",
  data: function(){
    return {
      files: [],
      password: '',
    };
  },
  methods: {
    handleFileDrop(e) {
      let droppedFiles = e.dataTransfer.files;
      if(!droppedFiles) return;
      ([...droppedFiles]).forEach(f => {
    this.files.push(f);
      });
    },
    handleFileInput(e) {
      let files = e.target.files;
      files = e.target.files
            if(!files) return;
      ([...files]).forEach(f => {

    this.files.push(f);
      });
    },
    removeFile(fileKey){
      this.files.splice(fileKey, 1)
    },
    fileDragIn(){
      this.color="white"
    },
     importValidator(){
    //to do import
    }
  },
};
</script>

<style>

body,html{
  height: 100%;
}

#app {
  height: 100vh;
}

main {
  margin-top: 30px;
  height: 100%;
}

.file-wrapper {
  text-align: center;
  margin: auto;
  width: 100%;
  border: 3px solid #24a0ed;
  padding: 10px;
  position: relative;
  overflow: hidden
}

.file-wrapper input {
    position: absolute;
    top: 0;
    right: 0;
    cursor: pointer;
    opacity: 0.0;
    filter: alpha(opacity=0);
    font-size: 300px;
    height: 200px;
}

.key-files {
  display: flex;
  text-align: left;
}

</style>
