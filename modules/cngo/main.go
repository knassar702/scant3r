
package main

import (
	"bufio"
	"context"
	"fmt"
	"net"
	"os"
	"strings"
	"sync"
	"time"
	"github.com/gookit/color"
	"github.com/jessevdk/go-flags"
)

// Setting Options For Args

var opts struct {
	// File name arg (required to run Script)
	File string `short:"f" long:"file" description:"Subdomains File" required:"true"`
	// Timeout For the http get Requets
	Timeout int `short:"t" long:"timeout" description:"Timeout For Requests" `
	// Concurrency For the http requests (something like threads)
	Concurrency int `short:"c" long:"concurrency" default:"25" description:"Concurrency For Requests"`
}

// Setting errors,domains,cnames color to print
var (
	erColor  = color.Style{color.BgRed, color.OpBold}.Render
	domColor = color.Style{color.FgYellow, color.OpBold}.Render
	cnColor  = color.Style{color.FgLightMagenta, color.OpBold}.Render
)

func main() {
	// Flage the args to start use it
	_, err := flags.Parse(&opts)
	// Check if the parse occurred any error
	if err != nil {
		fmt.Println(erColor("try to use -h to show the options and usage :)"))
		return
	}
	// naming the options
	filename := opts.File
	// setting timeout
	timeout := time.Duration(opts.Timeout * 1000000)
	concurrency := opts.Concurrency

	// Check if file not exists exit script
	if !isExists(filename) {
		fmt.Println(erColor("File Not Found"))
		return
	}
	// Start reading the file and pass urls channel to function to store the lines on it
	urls := getlines(filename)
	// set the WaitGroup
	var wg sync.WaitGroup
	// Start the concurrency and goroutine
	for i := 0; i < concurrency; i++ {
		// Add 1 every concurrency
		wg.Add(1)
		go func() {
			// Done the sync
			defer wg.Done()
			// Start Reading urls from channel
			for domain := range urls {
				// Pass url chan and timeout to return domain and cname
				domain, cname := getCname(domain, timeout)
				// Check if this url has no cname
				if len(cname) == 0 {
					fmt.Println(domColor(domain) + " -> " + erColor("has no Cname"))
				} else {
					// Remove the last dot in cname
					cname = strings.Trim(cname, ".")
					fmt.Println(domColor(domain) + " -> " + cnColor(cname))
				}
			}
		}()
	}
	// Wait untill workers finish
	wg.Wait()
}

// Cname function
func getCname(domain string, timeout time.Duration) (string, string) {
	// Configure Resolver
	r := &net.Resolver{
		// Passing the Context and address
		Dial: func(ctx context.Context, network, address string) (net.Conn, error) {
			d := net.Dialer{
				// Setting Timeout
				Timeout: timeout,
			}
			// Configure the dns server
			return d.DialContext(ctx, "udp", "8.8.4.4:53")
		},
	}
	// Getting the CNAME
	cname, err := r.LookupCNAME(context.Background(), domain)
	if err != nil {
		//panic(err)
	}
	return domain, string(cname)
}

// Get Urls From File Function
func getlines(filename string) <-chan string {
	// Create a channel to store the lines into it
	out := make(chan string)
	f, _ := os.Open(filename)
	// Create Scanner to read lines
	sc := bufio.NewScanner(f)
	// looping the scanner
	go func() {
		defer f.Close()
		defer close(out)
		for sc.Scan() {
			// Convert urls to lower and pass to channel
			domain := strings.ToLower(sc.Text())
			// Store lines into channels
			out <- domain
		}
	}()
	return out
}

// Check if file exists
func isExists(filename string) bool {
	// Passing the filename and use isnotexists to return file is exists or not
	if _, err := os.Stat(filename); os.IsNotExist(err) {
		return false
	}
	return true
}


