---
title: Understanding the Raft Consensus Algorithm
date: '2024-09-12'
draft: false
tags:
- distributed-systems
- consensus
- programming
summary: A practical walkthrough of leader election and log replication in Raft, with
  annotated Go examples.
---

Raft was designed to be understandable. Unlike Paxos, which often feels like reading ancient Greek while standing on your head, Raft splits the consensus problem into three distinct, manageable pieces: leader election, log replication, and safety.

## Leader Election

The core of Raft is the heartbeat mechanism. A leader sends periodic heartbeats to all followers. If a follower doesn't receive a heartbeat within the election timeout, it assumes the leader is dead and starts an election.

{{< tip title="Timer Jitter" >}}
To prevent split votes where every node times out simultaneously, Raft requires randomized election timeouts (e.g., between 150ms and 300ms).
{{< /tip >}}

## The Go Implementation

Here is a simplified look at how a heartbeat loop might be structured in Go using channels and tickers:

{{< highlight-file name="raft_leader.go" lang="go" >}}
func (rf *Raft) heartbeatLoop() {
    ticker := time.NewTicker(75 * time.Millisecond)
    defer ticker.Stop()

    for {
        select {
        case <-ticker.C:
            if rf.role == Leader {
                rf.broadcastAppendEntries()
            }
        case <-rf.shutdownCh:
            return
        }
    }
}
{{< /highlight-file >}}

When things go wrong, the logs are your best friend. But nothing replaces a solid understanding of the State Machine Replication fundamentals.