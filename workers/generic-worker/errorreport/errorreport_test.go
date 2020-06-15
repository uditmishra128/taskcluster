package errorreport

import (
	"fmt"
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
	"github.com/taskcluster/taskcluster/v30/internal/workerproto"
	workerProtoTesting "github.com/taskcluster/taskcluster/v30/internal/workerproto/testing"
)

func setupProtocols() (*workerproto.Protocol, *workerproto.Protocol) {
	workerTransp, runnerTransp := workerProtoTesting.NewLocalTransportPair()
	workerProto := workerproto.NewProtocol(workerTransp)
	workerProto.AddCapability("error-report")
	workerProto.Start(true)

	runnerProto := workerproto.NewProtocol(runnerTransp)
	runnerProto.AddCapability("error-report")
	return workerProto, runnerProto
}

func TestSendEmptyExtra(t *testing.T) {
	errorReported := false

	workerProto, runnerProto := setupProtocols()

	runnerProto.Register("error-report", func(msg workerproto.Message) {
		assert.Contains(t, msg.Properties, "title")
		assert.Equal(t, "generic-worker error", msg.Properties["title"])
		assert.Contains(t, msg.Properties, "kind")
		assert.Equal(t, "error", msg.Properties["kind"])
		assert.Contains(t, msg.Properties, "description")
		assert.Equal(t, "test error", msg.Properties["description"].(string))
		assert.Contains(t, msg.Properties, "extra")
		assert.Equal(t, msg.Properties["extra"], map[string]interface{}{})
		errorReported = true
	})

	runnerProto.Start(false)
	runnerProto.WaitUntilInitialized()

	// report test error
	Send(workerProto, fmt.Errorf("test error"), nil)

	for i := 0; i < 200; i++ {
		if !errorReported {
			time.Sleep(time.Millisecond * 10)
		} else {
			return
		}
	}
	t.Fatalf("No error-report was received")
}

func TestSendExtra(t *testing.T) {
	errorReported := false

	workerProto, runnerProto := setupProtocols()

	runnerProto.Register("error-report", func(msg workerproto.Message) {
		assert.Contains(t, msg.Properties, "extra")
		assert.Contains(t, msg.Properties["extra"], "kangaroo")
		assert.Contains(t, msg.Properties["extra"], "monster")
		assert.Equal(t, "pouches", msg.Properties["extra"].(map[string]interface{})["kangaroo"].(string))
		assert.Equal(t, "trucks", msg.Properties["extra"].(map[string]interface{})["monster"].(string))
		errorReported = true
	})

	runnerProto.Start(false)
	runnerProto.WaitUntilInitialized()

	// report test error
	Send(workerProto, fmt.Errorf("test error"), map[string]string{
		"kangaroo": "pouches",
		"monster":  "trucks",
	})

	for i := 0; i < 200; i++ {
		if !errorReported {
			time.Sleep(time.Millisecond * 10)
		} else {
			return
		}
	}
	t.Fatalf("No error-report was received")
}
