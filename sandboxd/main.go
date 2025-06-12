package main

import (
	"encoding/base64"
	"encoding/json"
	"flag"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"os/exec"
	"path/filepath"
)

type server struct {
	root string
}

type runRequest struct {
	Command string `json:"command"`
}

type runResponse struct {
	Output string `json:"output"`
	Error  string `json:"error,omitempty"`
}

type writeRequest struct {
	Path string `json:"path"`
	Data string `json:"data"` // base64 encoded
}

type readResponse struct {
	Data  string `json:"data"` // base64 encoded
	Error string `json:"error,omitempty"`
}

func (s *server) abs(rel string) string {
	return filepath.Join(s.root, filepath.Clean("/"+rel))
}

func (s *server) runHandler(w http.ResponseWriter, r *http.Request) {
	var req runRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}
	cmd := exec.Command("bash", "-c", req.Command)
	cmd.Dir = s.root
	out, err := cmd.CombinedOutput()
	resp := runResponse{Output: string(out)}
	if err != nil {
		resp.Error = err.Error()
	}
	json.NewEncoder(w).Encode(resp)
}

func (s *server) writeHandler(w http.ResponseWriter, r *http.Request) {
	var req writeRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}
	data, err := base64.StdEncoding.DecodeString(req.Data)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}
	p := s.abs(req.Path)
	if err := os.MkdirAll(filepath.Dir(p), 0755); err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	if err := ioutil.WriteFile(p, data, 0644); err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
}

func (s *server) readHandler(w http.ResponseWriter, r *http.Request) {
	p := r.URL.Query().Get("path")
	data, err := ioutil.ReadFile(s.abs(p))
	resp := readResponse{}
	if err != nil {
		resp.Error = err.Error()
	} else {
		resp.Data = base64.StdEncoding.EncodeToString(data)
	}
	json.NewEncoder(w).Encode(resp)
}

func (s *server) listHandler(w http.ResponseWriter, r *http.Request) {
	var files []string
	filepath.Walk(s.root, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}
		if !info.IsDir() {
			rel, _ := filepath.Rel(s.root, path)
			files = append(files, rel)
		}
		return nil
	})
	json.NewEncoder(w).Encode(files)
}

func main() {
	root := flag.String("root", "./sandbox", "sandbox root directory")
	addr := flag.String("addr", ":8080", "listen address")
	flag.Parse()

	s := &server{root: *root}
	if err := os.MkdirAll(s.root, 0755); err != nil {
		log.Fatalf("failed to create root: %v", err)
	}

	http.HandleFunc("/run", s.runHandler)
	http.HandleFunc("/write", s.writeHandler)
	http.HandleFunc("/read", s.readHandler)
	http.HandleFunc("/list", s.listHandler)

	fmt.Printf("Sandbox daemon running on %s\n", *addr)
	log.Fatal(http.ListenAndServe(*addr, nil))
}
