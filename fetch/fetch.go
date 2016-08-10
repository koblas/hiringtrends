package main

import (
    "strconv"
    "os"
    "fmt"
    "path/filepath"
    "io/ioutil"
    "net/http"
    "encoding/json"
)

type User struct {
    Id  string `json:"id"`
    Delay  int `json:"delay"`
    Created  int `json:"created"`
    Karma  int `json:"karma"`
    About  string `json:"about"`
    Submitted  []int `json:"submitted"`
}

type Post struct {
    Id  int `json:"id"`
    Deleted  bool `json:"deleted"`
    Type  string `json:"type"`
    By  string `json:"by"`
    Created  int `json:"time"`
    Text  string `json:"text"`
    Dead  bool `json:"dead"`
    Parent  *int `json:"parent"`
    Kids  []int `json:"kids"`
    Url  string `json:"url"`
    Score  int `json:"score"`
    Title  string `json:"title"`
    Parts  []int `json:"parts"`
    Descendants  int `json:"descendants"`
}

const (
    URL_BASE = "https://hacker-news.firebaseio.com/v0"
)

func main() {
    if len(os.Args) == 1 {
        usage()
    }

    // user_submissions("whoishiring", os.Args[1])
    // user_submissions("_whoishiring", os.Args[1])

    do_post(3300290, os.Args[1])    // December 2011 canonical post
}

func user_submissions(name string, dir string) {
    user, err := fetchUser(name)
    if err != nil {
        fmt.Fprintf(os.Stderr, "Unable to get the %s user from HN\n", name)
        os.Exit(1)
    }

    for _, id := range user.Submitted {
        if id == 3300371 {  // Invalid post for December 2011
            continue
        }
        do_post(id, dir)
    }
}

func do_post(id int, dir string) {
    err := os.Mkdir(filepath.Join(dir, strconv.Itoa(id)), 0777)

    post, err := fetchPost(id)
    if err != nil {
        panic(err)
    }

    fmt.Printf("Starting id=%d title=\"%s\"\n", post.Id, post.Title)

    writePost(post, filepath.Join(dir, strconv.Itoa(post.Id), strconv.Itoa(post.Id) + ".json"))

    // fmt.Println(post)
    for _, cid := range post.Kids {
        comment, err := fetchPost(cid)
        if err != nil {
            fmt.Printf("Error fetching: %v\n", err)
            continue
        }

        writePost(comment, filepath.Join(dir, strconv.Itoa(post.Id), strconv.Itoa(comment.Id) + ".json"))
    }
}

func usage() {
    fmt.Fprintf(os.Stderr, "Usage: %s DIRECTORY\n", filepath.Base(os.Args[0]))
    os.Exit(1)
}

// Write a post object to the file system in JSON format
func writePost(post *Post, path string) {
    f, err := os.Create(path)

    if err != nil {
        fmt.Printf("Error saving: %v\n", err)
        return
    }
    defer f.Close()

    b, err := json.Marshal(post)
    if err != nil {
        fmt.Printf("Error marshal: %v\n", err)
        return
    }
    f.Write(b)
    f.Write([]byte("\n"))
}

// Fetch something and return the bytes of the body
func fetch(url string) ([]byte, error) {
    resp, err := http.Get(url)
    if err != nil {
        return nil, err
    }

    defer resp.Body.Close()
    return ioutil.ReadAll(resp.Body)
}

// Fetch the post object from the HackerNews API
func fetchPost(id int) (*Post, error) {
    body, err := fetch(fmt.Sprintf("%s/item/%d.json", URL_BASE, id))
    if err != nil {
        return nil, err
    }

    post := Post{}
    if err := json.Unmarshal(body, &post); err != nil {
        return nil, err
    }

    return &post, nil
}

// Fetch the user object from the HackerNews API
func fetchUser(name string) (*User, error) {
    body, err := fetch(fmt.Sprintf("%s/user/%s.json", URL_BASE, name))
    if err != nil {
        return nil, err
    }

    user := User{}
    if err := json.Unmarshal(body, &user); err != nil {
        return nil, err
    }

    return &user, nil
}
