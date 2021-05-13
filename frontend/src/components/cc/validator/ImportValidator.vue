<template>
  <div id="app" @dragover.prevent @drop.prevent>
    <div class="container" @drop="fileDragOut">
      <div class="row pb-3 pt-3">
        <h2>Import</h2>
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
                  v-b-trash.hover
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
            <b-form-group
              label="Validator password:"
              label-for="input-1"
              label-size="m"
            >
              <input
                v-model="password"
                type="password"
                placeholder="min.8 characters"
                title="Put key file's password here!"
                align="left"
              />
            </b-form-group>

            <b-button
              variant="primary"
              @click="importValidator()"
              :disabled="files.length === 0 || password.length < 8"
              title="import accounts"
            >
              Import
            </b-button>
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
  },
  computed: {
    // "no duplicate data filter" not used
    uniqFiles() {
      let uniqfiles = {};
      return this.files.filter((f) => {
        if (!(f.name in uniqfiles)) {
          uniqfiles[f.name] = true;
          return true;
        }
        else {
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
      }
      else {
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
      }
      else {
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
    importValidator() {
      //todo import
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
