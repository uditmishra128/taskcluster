package model

import (
	"encoding/json"
	"errors"
	"fmt"
	"sort"
	"strings"

	"github.com/taskcluster/jsonschema2go/text"
)

//////////////////////////////////////////////////////////////////
//
// From: http://schemas.taskcluster.net/base/v1/api-reference.json
//
//////////////////////////////////////////////////////////////////

// API represents the HTTP interface of a Taskcluster service
type API struct {
	*APIReferenceFile
	apiDef *APIDefinition
}

func (api *API) String() string {
	result := fmt.Sprintf(
		"Version     = '%v'\n"+
			"Schema      = '%v'\n"+
			"Title       = '%v'\n"+
			"Description = '%v'\n"+
			"Base URL    = '%v'\n",
		api.Version, api.Schema, api.Title, api.Description, api.BaseURL,
	)
	for i, entry := range api.Entries {
		result += fmt.Sprintf("Entry %-6v=\n%v", i, entry.String())
	}
	return result
}

func (api *API) postPopulate(apiDef *APIDefinition) {

	// make sure each entry defined for this API has a unique generated method name
	api.apiDef.members = make(map[string]bool)

	for i := range api.Entries {
		api.Entries[i].Parent = api
		api.Entries[i].MethodName = text.GoIdentifierFrom(api.Entries[i].Name, true, api.apiDef.members)
		api.Entries[i].postPopulate(apiDef)
	}
}

func (api *API) generateAPICode(apiName string) string {
	// package name and variable name are ideally not the same
	// so find a way to make them different...
	// also don't allow type variable name to be the same as
	// the type name
	// e.g. switch case of first character, and if first
	// character is not can't switch case for whatever
	// reason, prefix variable name with "my"
	exampleVarName := api.apiDef.ExampleVarName
	var exampleCall string
	// here we choose an example API method to call, just the first one in the list of api.Entries
	// We need to first see if it returns one or two variables...
	if api.Entries[0].Output == "" {
		exampleCall = "//  err := " + exampleVarName + "." + api.Entries[0].MethodName + "(.....)"
	} else {
		exampleCall = "//  data, err := " + exampleVarName + "." + api.Entries[0].MethodName + "(.....)"
	}
	comment := ""
	if api.Description != "" {
		comment = text.Indent(api.Description, "// ")
	}
	if len(comment) >= 1 && comment[len(comment)-1:] != "\n" {
		comment += "\n"
	}
	comment += "//\n"
	comment += fmt.Sprintf("// See: %v\n", api.apiDef.DocRoot)
	comment += "//\n"
	comment += "// How to use this package\n"
	comment += "//\n"
	comment += "// First create " + text.IndefiniteArticle(api.apiDef.Name) + " " + api.apiDef.Name + " object:\n"
	comment += "//\n"
	comment += "//  " + exampleVarName + " := " + api.apiDef.PackageName + ".New(nil)\n"
	comment += "//\n"
	comment += "// and then call one or more of " + exampleVarName + "'s methods, e.g.:\n"
	comment += "//\n"
	comment += exampleCall + "\n"
	comment += "//\n"
	comment += "// handling any errors...\n"
	comment += "//\n"
	comment += "//  if err != nil {\n"
	comment += "//  	// handle error...\n"
	comment += "//  }\n"
	comment += "//\n"
	comment += "// Taskcluster Schema\n"
	comment += "//\n"
	comment += "// The source code of this go package was auto-generated from the API definition at\n"
	comment += "// " + api.apiDef.URL + " together with the input and output schemas it references, downloaded on\n"
	comment += "// " + downloadedTime.UTC().Format("Mon, 2 Jan 2006 at 15:04:00 UTC") + ". The code was generated\n"
	comment += "// by https://github.com/taskcluster/taskcluster-client-go/blob/master/build.sh.\n"

	content := comment
	content += "package " + api.apiDef.PackageName + "\n"

	// note: we remove unused imports later, so e.g. if net/url is not used, it
	// will get removed later using:
	// https://godoc.org/golang.org/x/tools/imports

	content += `
import (
	"encoding/json"
	"errors"
	"net/url"
	"time"
	tcclient "github.com/taskcluster/taskcluster-client-go"
)

const (
	DefaultBaseURL = "` + api.BaseURL + `"
)

type ` + api.apiDef.Name + ` tcclient.Client

// New returns ` + text.IndefiniteArticle(api.apiDef.Name) + ` ` + api.apiDef.Name + ` client, configured to run against production. Pass in
// nil to create a client without authentication. The
// returned client is mutable, so returned settings can be altered.
//
`
	// Here we want to add spaces between commands and comments, such that the comments line up, e.g.:
	//
	//  myQueue, credsError := queue.New(nil)                    // credentials loaded from TASKCLUSTER_* environment variables
	//  if credsError != nil {
	//      // handle malformed credentials...
	//  }
	//  myQueue.Authenticate = false                             // disable authentication (creds above are now ignored)
	//  myQueue.BaseURL = "http://localhost:1234/api/Queue/v1"   // alternative API endpoint (production by default)
	//  data, err := myQueue.Task(.....)                         // for example, call the Task(.....) API endpoint (described further down)...
	//
	// We do this by generating the code, then calculating the max length of one of the code lines,
	// and then padding with spaces based on max line length and adding comments.

	commentedSection := [][]string{
		{
			"//  " + exampleVarName + " := " + api.apiDef.PackageName + ".New(nil)",
			"// client without authentication",
		},
		{
			"//  " + exampleVarName + ".BaseURL = \"http://localhost:1234/api/" + apiName + "/v1\"",
			"// alternative API endpoint (production by default)",
		},
		{
			exampleCall,
			"// for example, call the " + api.Entries[0].MethodName + "(.....) API endpoint (described further down)...",
		},
	}

	maxLength := 0
	for _, j := range commentedSection {
		if len(j[0]) > maxLength {
			maxLength = len(j[0])
		}
	}
	for _, j := range commentedSection {
		if len(j[1]) > 0 {
			content += j[0] + strings.Repeat(" ", maxLength-len(j[0])+3) + j[1] + "\n"
		} else {
			content += j[0] + "\n"
		}
	}

	content += "//  if err != nil {\n"
	content += "//  	// handle errors...\n"
	content += "//  }"
	content += `
func New(credentials *tcclient.Credentials) *` + api.apiDef.Name + ` {
	return &` + api.apiDef.Name + `{
		Credentials: credentials,
		BaseURL: DefaultBaseURL,
		Authenticate: credentials != nil,
	}
}

// NewFromEnv returns ` + text.IndefiniteArticle(api.apiDef.Name) + ` ` + api.apiDef.Name + ` client with credentials taken from the environment variables:
//
//  TASKCLUSTER_CLIENT_ID
//  TASKCLUSTER_ACCESS_TOKEN
//  TASKCLUSTER_CERTIFICATE
//
// If environment variables TASKCLUSTER_CLIENT_ID is empty string or undefined
// authentication will be disabled.
func NewFromEnv(credentials *tcclient.Credentials) *` + api.apiDef.Name + ` {
	c := tcclient.CredentialsFromEnvVars()
	return &` + api.apiDef.Name + `{
		Credentials: c,
		BaseURL: DefaultBaseURL,
		Authenticate: c.ClientID != "",
	}
}

`
	for _, entry := range api.Entries {
		content += entry.generateAPICode(apiName)
	}
	return content
}

func (api *API) setAPIDefinition(apiDef *APIDefinition) {
	api.apiDef = apiDef
}

// APIEntry represents an individual HTTP API call
// of a Taskcluster service
type APIEntry struct {
	*Entry
	MethodName string
	Parent     *API
}

// Add entry.Input and entry.Output to schemaURLs, if they are set
func (entry *APIEntry) postPopulate(apiDef *APIDefinition) {
	for _, v := range []string{
		entry.Input,
		entry.Output,
	} {
		if x := &entry.Parent.apiDef.schemaURLs; v != "" {
			*x = append(*x, v)
		}
	}
}

func (entry *APIEntry) String() string {
	return fmt.Sprintf(
		"    Entry Type        = '%v'\n"+
			"    Entry Method      = '%v'\n"+
			"    Entry Route       = '%v'\n"+
			"    Entry Args        = '%v'\n"+
			"    Entry Query        = '%v'\n"+
			"    Entry Name        = '%v'\n"+
			"    Entry Stability   = '%v'\n"+
			"    Entry Scopes      = '%v'\n"+
			"    Entry Input       = '%v'\n"+
			"    Entry Output      = '%v'\n"+
			"    Entry Title       = '%v'\n"+
			"    Entry Description = '%v'\n",
		entry.Type, entry.Method, entry.Route, entry.Args,
		entry.Query, entry.Name, entry.Stability, &entry.Scopes,
		entry.Input, entry.Output, entry.Title, entry.Description,
	)
}

func (entry *APIEntry) generateAPICode(apiName string) string {
	content := entry.generateDirectMethod(apiName)
	if strings.ToUpper(entry.Method) == "GET" {
		content += entry.generateSignedURLMethod(apiName)
	}
	return content
}

func (entry *APIEntry) getInputParamsAndQueryStringCode() (inputParams, queryCode, queryExpr string) {
	inputArgs := append([]string{}, entry.Args...)

	// add optional query parameters
	queryCode = ""
	queryExpr = "nil"
	if len(entry.Query) > 0 {
		queryExpr = "v"
		sort.Strings(entry.Query)
		queryCode = "v := url.Values{}\n"
		for _, j := range entry.Query {
			inputArgs = append(inputArgs, j)
			queryCode += "if " + j + " != \"\" {\n\tv.Add(\"" + j + "\", " + j + ")\n}\n"
		}
	}
	// all input parameters are strings, so if there are any, add the type to show it
	if len(inputArgs) > 0 {
		inputParams += strings.Join(inputArgs, ", ") + " string"
	}
	return
}

func (entry *APIEntry) generateDirectMethod(apiName string) string {
	comment := ""
	if entry.Stability != "stable" {
		comment += "// Stability: *** " + strings.ToUpper(entry.Stability) + " ***\n"
		comment += "//\n"
	}
	if entry.Description != "" {
		comment += text.Indent(entry.Description, "// ")
	}
	if len(comment) >= 1 && comment[len(comment)-1:] != "\n" {
		comment += "\n"
	}
	comment += requiredScopesComment(&entry.Scopes)
	comment += "//\n"
	comment += fmt.Sprintf("// See %v#%v\n", entry.Parent.apiDef.DocRoot, entry.Name)

	inputParams, queryCode, queryExpr := entry.getInputParamsAndQueryStringCode()

	apiArgsPayload := "nil"
	if entry.Input != "" {
		apiArgsPayload = "payload"
		p := "payload *" + entry.Parent.apiDef.schemas.SubSchema(entry.Input).TypeName
		if inputParams == "" {
			inputParams = p
		} else {
			inputParams += ", " + p
		}
	}

	responseType := "error"
	if entry.Output != "" {
		responseType = "(*" + entry.Parent.apiDef.schemas.SubSchema(entry.Output).TypeName + ", error)"
	}

	content := comment
	content += "func (" + entry.Parent.apiDef.ExampleVarName + " *" + entry.Parent.apiDef.Name + ") " + entry.MethodName + "(" + inputParams + ") " + responseType + " {\n"
	content += queryCode
	content += "\tcd := tcclient.Client(*" + entry.Parent.apiDef.ExampleVarName + ")\n"
	if entry.Output != "" {
		content += "\tresponseObject, _, err := (&cd).APICall(" + apiArgsPayload + ", \"" + strings.ToUpper(entry.Method) + "\", \"" + strings.Replace(strings.Replace(entry.Route, "<", "\" + url.QueryEscape(", -1), ">", ") + \"", -1) + "\", new(" + entry.Parent.apiDef.schemas.SubSchema(entry.Output).TypeName + "), " + queryExpr + ")\n"
		content += "\treturn responseObject.(*" + entry.Parent.apiDef.schemas.SubSchema(entry.Output).TypeName + "), err\n"
	} else {
		content += "\t_, _, err := (&cd).APICall(" + apiArgsPayload + ", \"" + strings.ToUpper(entry.Method) + "\", \"" + strings.Replace(strings.Replace(entry.Route, "<", "\" + url.QueryEscape(", -1), ">", ") + \"", -1) + "\", nil, " + queryExpr + ")\n"
		content += "\treturn err\n"
	}
	content += "}\n"
	content += "\n"
	// can remove any code that added an empty string to another string
	return strings.Replace(content, ` + ""`, "", -1)
}

func (entry *APIEntry) generateSignedURLMethod(apiName string) string {
	// if no required scopes, no reason to provide a signed url
	// method, since no auth is required, so unsigned url already works
	if entry.Scopes.Type == "" {
		return ""
	}
	comment := "// Returns a signed URL for " + entry.MethodName + ", valid for the specified duration.\n"
	comment += requiredScopesComment(&entry.Scopes)
	comment += "//\n"
	comment += fmt.Sprintf("// See %v for more details.\n", entry.MethodName)
	inputParams, queryCode, queryExpr := entry.getInputParamsAndQueryStringCode()
	if inputParams == "" {
		inputParams = "duration time.Duration"
	} else {
		inputParams += ", duration time.Duration"
	}

	content := comment
	content += "func (" + entry.Parent.apiDef.ExampleVarName + " *" + entry.Parent.apiDef.Name + ") " + entry.MethodName + "_SignedURL(" + inputParams + ") (*url.URL, error) {\n"
	content += queryCode
	content += "\tcd := tcclient.Client(*" + entry.Parent.apiDef.ExampleVarName + ")\n"
	content += "\treturn (&cd).SignedURL(\"" + strings.Replace(strings.Replace(entry.Route, "<", "\" + url.QueryEscape(", -1), ">", ") + \"", -1) + "\", " + queryExpr + ", duration)\n"
	content += "}\n"
	content += "\n"
	// can remove any code that added an empty string to another string
	return strings.Replace(content, ` + ""`, "", -1)
}

func requiredScopesComment(scopes *ScopeExpressionTemplate) string {
	if scopes.Type == "" {
		return ""
	}
	comment := "\n"
	comment += "Required scopes:\n"
	comment += text.Indent(scopes.String()+"\n", "  ")
	return text.Indent(comment, "// ")
}

func (scopes *ScopeExpressionTemplate) String() string {
	switch scopes.Type {
	case "":
		return ""
	case "AllOf":
		return scopes.AllOf.String()
	case "AnyOf":
		return scopes.AnyOf.String()
	case "ForEachIn":
		return scopes.ForEachIn.String()
	case "IfThen":
		return scopes.IfThen.String()
	case "RequiredScope":
		return scopes.RequiredScope.String()
	default:
		panic(fmt.Sprintf("Internal error - did not recognise scope form '%v'", scopes.Type))
	}
}

func (allOf *AllOf) String() string {
	if allOf == nil {
		return "WARNING: NIL AllOf"
	}
	switch len(allOf.AllOf) {
	case 0:
		return ""
	case 1:
		return allOf.AllOf[0].String()
	}
	var desc string
	for _, exp := range allOf.AllOf {
		x := text.Indent(exp.String(), "  ")
		if len(x) >= 2 {
			desc += "\n" + "* " + x[2:]
		}
	}
	return "All of:" + desc
}

func (anyOf *AnyOf) String() string {
	if len(anyOf.AnyOf) == 0 {
		return "AnyOf empty set - INVALID"
	}
	if len(anyOf.AnyOf) == 1 {
		return anyOf.AnyOf[0].String()
	}
	var desc string
	for _, exp := range anyOf.AnyOf {
		x := text.Indent(exp.String(), "  ")
		if len(x) >= 2 {
			desc += "\n" + "- " + x[2:]
		}
	}
	return "Any of:" + desc
}

func (forEachIn *ForEachIn) String() string {
	return "For " + forEachIn.For + " in " + forEachIn.In + " each " + forEachIn.Each
}

func (ifThen *IfThen) String() string {
	return "If " + ifThen.If + ":\n" + text.Indent(ifThen.Then.String(), "  ")
}

func (rs *RequiredScope) String() string {
	return string(*rs)
}

// MarshalJSON calls json.RawMessage method of the same name. Required since
// ScopeExpressionTemplate is of type json.RawMessage...
func (this *ScopeExpressionTemplate) MarshalJSON() ([]byte, error) {
	return (this.RawMessage).MarshalJSON()
}

// UnmarshalJSON identifies the data structure at runtime, and unmarshals in
// the appropriate type
func (this *ScopeExpressionTemplate) UnmarshalJSON(data []byte) error {
	if this == nil {
		return errors.New("ScopeExpressionTemplate: UnmarshalJSON on nil pointer")
	}
	this.RawMessage = append((this.RawMessage)[0:0], data...)
	var tempObj interface{}
	err := json.Unmarshal(this.RawMessage, &tempObj)
	if err != nil {
		panic("Internal error: " + err.Error())
	}
	switch t := tempObj.(type) {
	case string:
		this.Type = "RequiredScope"
		this.RequiredScope = new(RequiredScope)
		*(this.RequiredScope) = RequiredScope(t)
	case map[string]interface{}:
		j, err := json.Marshal(t)
		if err != nil {
			panic("Internal error: " + err.Error())
		}
		if _, exists := t["AnyOf"]; exists {
			this.Type = "AnyOf"
			this.AnyOf = new(AnyOf)
			err = json.Unmarshal(j, this.AnyOf)
		}
		if _, exists := t["AllOf"]; exists {
			this.Type = "AllOf"
			this.AllOf = new(AllOf)
			err = json.Unmarshal(j, this.AllOf)
		}
		if _, exists := t["if"]; exists {
			this.Type = "IfThen"
			this.IfThen = new(IfThen)
			err = json.Unmarshal(j, this.IfThen)
		}
		if _, exists := t["for"]; exists {
			this.Type = "ForEachIn"
			this.ForEachIn = new(ForEachIn)
			err = json.Unmarshal(j, this.ForEachIn)
		}
		if err != nil {
			panic("Internal error: " + err.Error())
		}
	// for old style scopesets [][]string (normal disjunctive form)
	case []interface{}:
		this.Type = "AnyOf"
		this.AnyOf = &AnyOf{
			AnyOf: make([]ScopeExpressionTemplate, len(t), len(t)),
		}
		for i, j := range t {
			allOf := j.([]interface{})
			this.AnyOf.AnyOf[i] = ScopeExpressionTemplate{
				Type: "AllOf",
				AllOf: &AllOf{
					AllOf: make([]ScopeExpressionTemplate, len(allOf), len(allOf)),
				},
			}
			for k, l := range allOf {
				rs := RequiredScope(l.(string))
				this.AnyOf.AnyOf[i].AllOf.AllOf[k] = ScopeExpressionTemplate{
					Type:          "RequiredScope",
					RequiredScope: &rs,
				}
			}
		}
	default:
		panic(fmt.Sprintf("Internal error: unrecognised type %T", t))
	}
	return nil
}
