<template>
  <div id="app" @dragover.prevent @drop.prevent>
    <div class="container" @drop="fileDragOut">
      <div class="row pb-3 pt-3">
        <h2>Import Validators</h2>
      </div>

      <div
        class="file-wrapper"
        @dragleave="fileDragOut"
        @dragover="fileDragIn"
        @drop="handleFileDrop"
        v-bind:style="{ 'background-color': color }"
      >
        <input
          type="file"
          name="file-input"
          multiple="true"
          accept="application/JSON"
          @change="handleFileInput"
          title="Put your key files here!"
        />
        Click or drag to insert key files
      </div>

      <div>
        <table class="table table-striped table-hover">
          <thead>
            <tr>
              <th>Number</th>
              <th>Key file</th>
              <th>Action</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="(file, index) in files" v-bind:key="file && index">
              <td>
                {{ index + 1 }}
              </td>

              <td>
                {{ file.name }}
              </td>

              <td>
                <b-button
                  size="sm"
                  @click="removeFile(index)"
                  variant="primary"
                  class="mb-2 mr-sm-2 mb-sm-0"
                  title="remove file"
                >
                  <b-icon icon="trash" aria-hidden="true"></b-icon>
                </b-button>
              </td>
            </tr>
          </tbody>
        </table>

        <div class="container pb-3 pt-3">
          <p class="text-left">
            <b-form inline>
              <label class="mb-2 mr-sm-2 mb-sm-0" for="inline-new-url">
                Validators' password:
              </label>
              <b-form-input
                v-model="password"
                type="password"
                placeholder="Validators' password"
                align="left"
                class="mb-2 mr-sm-2 mb-sm-0 w-50"
              />

              <b-button
                variant="primary"
                @click="importValidator"
                :disabled="files.length === 0"
                title="import accounts"
              >
                Import
              </b-button>
            </b-form>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ImportValidator",
  components: {},
  data() {
    return {
      files: [],
      color: "#87cefa",
      password: "",
    };
  },
  props: {
    ethereum2config: Object,
    processChange: Function,
  },
  computed: {
    // "no duplicate data filter" not used
    uniqFiles() {
      let uniqfiles = {};
      return this.files.filter((f) => {
        if (!(f.name in uniqfiles)) {
          uniqfiles[f.name] = true;
          return true;
        } else {
          return false;
        }
      });
    },
  },
  methods: {
    handleFileDrop(e) {
      let droppedFiles = e.dataTransfer.files;
      if (!droppedFiles) return;
      if (this.files.length == 0) {
        [...droppedFiles].forEach((df) => {
          this.files.push(df);
        });
      } else {
        [...droppedFiles].forEach((df) => {
          let exists = false;
          [...this.files].forEach((f) => {
            if (df.name == f.name) {
              exists = true;
            }
          });
          if (exists == false) {
            this.files.push(df);
          }
        });
      }
    },
    handleFileInput(e) {
      let files = e.target.files;
      files = e.target.files;
      if (!files) return;
      if (this.files.length == 0) {
        [...files].forEach((f) => {
          this.files.push(f);
        });
      } else {
        [...files].forEach((f) => {
          let exists = false;
          [...this.files].forEach((fi) => {
            if (f.name == fi.name) {
              exists = true;
            }
          });
          if (exists == false) {
            this.files.push(f);
          }
        });
      }
    },
    removeFile(fileKey) {
      this.files.splice(fileKey, 1);
    },
    fileDragIn() {
      this.color = "white";
    },
    fileDragOut() {
      this.color = "#87cefa";
    },
    async importValidator() {
      let jsonFiles = [];
      let i = 0;
      for (i = 0; i < this.files.length; i++){
        let jsonContent = await this.readFile(this.files[i]);
        jsonFiles.push({
          name: this.files[i].name,
          content: jsonContent,
        });
      }

      console.log(jsonFiles);
      console.log(jsonFiles[0].content);
      console.log(jsonFiles[0].content.value);

      this.processChange("import-validator-accounts", 100, {
        validator_password: this.password,
        validator_keys: jsonFiles,
      });
    },

    readFile: async function(file) {
      return new Promise((resolve, reject) => {
        let reader = new FileReader();
        reader.readAsText(file, "UTF-8");
        reader.onload =  evt => {
          resolve(evt.target.result);
        }
        reader.onerror = evt => {
          reject(evt);
        }
      });
    },

    sleep(milliseconds) {
      return new Promise(resolve => setTimeout(resolve, milliseconds));
    },
  },
};
</script>

<style>
#app {
  height: 100vh;
}
.file-wrapper {
  text-align: center;
  width: 100%;
  border: 3px inset #24a0ed;
  padding: 15px;
  position: relative;
  overflow: hidden;
}
.file-wrapper input {
  position: absolute;
  top: 0;
  right: 0;
  cursor: pointer;
  opacity: 0;
  filter: alpha(opacity=0);
  font-size: 300px;
  height: 200px;
}
</style>
