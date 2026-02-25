"""
Ethereum vs Polkadot: A Comprehensive Comparison
=================================================
This script compares key technical and ecosystem attributes
of the Ethereum and Polkadot blockchain platforms.
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class BlockchainProfile:
    name: str
    native_token: str
    launched: int
    consensus: str
    tps: str                        # transactions per second
    finality: str
    smart_contracts: bool
    smart_contract_language: List[str]
    scalability_approach: str
    governance: str
    sharding: bool
    interoperability: str
    energy_efficient: bool
    notable_feature: str
    avg_tx_fee: str

    def display(self):
        print(f"\n{'=' * 50}")
        print(f"  {self.name.upper()}")
        print(f"{'=' * 50}")
        print(f"  Native Token          : {self.native_token}")
        print(f"  Launched              : {self.launched}")
        print(f"  Consensus Mechanism   : {self.consensus}")
        print(f"  Throughput (TPS)      : {self.tps}")
        print(f"  Transaction Finality  : {self.finality}")
        print(f"  Smart Contracts       : {'Yes' if self.smart_contracts else 'No'}")
        print(f"  Contract Languages    : {', '.join(self.smart_contract_language)}")
        print(f"  Scalability Approach  : {self.scalability_approach}")
        print(f"  Governance Model      : {self.governance}")
        print(f"  Sharding              : {'Yes' if self.sharding else 'No'}")
        print(f"  Interoperability      : {self.interoperability}")
        print(f"  Energy Efficient      : {'Yes' if self.energy_efficient else 'No'}")
        print(f"  Avg. Transaction Fee  : {self.avg_tx_fee}")
        print(f"  Notable Feature       : {self.notable_feature}")


def compare(eth: BlockchainProfile, dot: BlockchainProfile):
    attributes = [
        ("Native Token",        eth.native_token,               dot.native_token),
        ("Launched",            str(eth.launched),               str(dot.launched)),
        ("Consensus",           eth.consensus,                   dot.consensus),
        ("TPS",                 eth.tps,                         dot.tps),
        ("Finality",            eth.finality,                    dot.finality),
        ("Smart Contracts",     "Yes" if eth.smart_contracts else "No",
                                "Yes" if dot.smart_contracts else "No"),
        ("Contract Languages",  ", ".join(eth.smart_contract_language),
                                ", ".join(dot.smart_contract_language)),
        ("Scalability",         eth.scalability_approach,        dot.scalability_approach),
        ("Governance",          eth.governance,                  dot.governance),
        ("Sharding",            "Yes" if eth.sharding else "No",
                                "Yes" if dot.sharding else "No"),
        ("Interoperability",    eth.interoperability,            dot.interoperability),
        ("Energy Efficient",    "Yes" if eth.energy_efficient else "No",
                                "Yes" if dot.energy_efficient else "No"),
        ("Avg. Tx Fee",         eth.avg_tx_fee,                  dot.avg_tx_fee),
        ("Notable Feature",     eth.notable_feature,             dot.notable_feature),
    ]

    col_w = 28
    header = f"\n{'ATTRIBUTE':<22}  {eth.name:<{col_w}}  {dot.name:<{col_w}}"
    print(header)
    print("-" * (22 + 2 + col_w + 2 + col_w))
    for label, ev, dv in attributes:
        print(f"{label:<22}  {ev:<{col_w}}  {dv:<{col_w}}")


def key_differences():
    print("""
KEY ARCHITECTURAL DIFFERENCES
------------------------------
1. DESIGN PHILOSOPHY
   • Ethereum  – A general-purpose smart-contract platform; one chain
                 that hosts all dApps directly.
   • Polkadot  – A "blockchain of blockchains" (relay chain + parachains)
                 focused on cross-chain communication.

2. SCALABILITY
   • Ethereum  – Scales via Layer-2 rollups (Optimism, Arbitrum, zkSync)
                 and future danksharding.
   • Polkadot  – Scales horizontally through up to 100 independent
                 parachains running in parallel.

3. INTEROPERABILITY
   • Ethereum  – Cross-chain bridges exist but are external and often
                 security-sensitive.
   • Polkadot  – Native Cross-Consensus Messaging (XCM) lets parachains
                 communicate trustlessly at the protocol level.

4. GOVERNANCE
   • Ethereum  – Off-chain; EIPs are debated by core devs and the
                 community; no on-chain voting for protocol changes.
   • Polkadot  – Fully on-chain via OpenGov: DOT holders vote on
                 referenda; the council and technical committee guide
                 upgrades without hard forks.

5. UPGRADES
   • Ethereum  – Requires hard forks coordinated across the ecosystem.
   • Polkadot  – Forkless runtime upgrades via WebAssembly; parachains
                 can upgrade independently.

6. SECURITY MODEL
   • Ethereum  – Each app shares Ethereum's validator set (monolithic).
   • Polkadot  – Shared security: all parachains are secured by the
                 relay chain's validator pool.

7. DEVELOPER ECOSYSTEM
   • Ethereum  – Largest ecosystem: Solidity, Hardhat, Foundry, vast
                 tooling, and the most DeFi/NFT dApps.
   • Polkadot  – Substrate framework (Rust) powers custom chains;
                 EVM-compatible parachains (Moonbeam) ease migration.
""")


def use_case_guide():
    print("""
WHEN TO CHOOSE WHICH?
------------------------------
  Choose ETHEREUM if you want to:
    ✓ Deploy Solidity / EVM smart contracts immediately
    ✓ Tap into the largest DeFi, NFT, and dApp ecosystem
    ✓ Benefit from the most battle-tested L2 rollup infrastructure

  Choose POLKADOT if you want to:
    ✓ Build a custom sovereign blockchain (parachain) with its own rules
    ✓ Enable trustless, native cross-chain communication (XCM)
    ✓ Leverage shared security without bootstrapping your own validators
    ✓ Iterate quickly with forkless on-chain upgrades
""")


def main():
    ethereum = BlockchainProfile(
        name="Ethereum",
        native_token="ETH",
        launched=2015,
        consensus="Proof-of-Stake (Gasper / LMD-GHOST + Casper FFG)",
        tps="~15–30 native; ~2,000–4,000 with L2 rollups",
        finality="~12–15 min (epoch finality) / ~12 s (slot)",
        smart_contracts=True,
        smart_contract_language=["Solidity", "Vyper", "Yul"],
        scalability_approach="Layer-2 rollups + future danksharding",
        governance="Off-chain EIP process; community/core-dev driven",
        sharding=False,          # danksharding planned but not yet live
        interoperability="External bridges; no native cross-chain protocol",
        energy_efficient=True,   # post-Merge PoS
        notable_feature="Largest smart-contract ecosystem & DeFi/NFT hub",
        avg_tx_fee="$0.50–$20 (variable gas; lower on L2s)",
    )

    polkadot = BlockchainProfile(
        name="Polkadot",
        native_token="DOT",
        launched=2020,
        consensus="Nominated Proof-of-Stake (NPoS) + GRANDPA / BABE",
        tps="~1,000 relay chain; ~100,000+ across all parachains",
        finality="~6 s (GRANDPA deterministic finality)",
        smart_contracts=True,
        smart_contract_language=["Rust (ink!)", "Solidity (via EVM parachains)"],
        scalability_approach="Parallel parachains (up to 100 chains)",
        governance="On-chain OpenGov; DOT-holder referenda & council",
        sharding=True,           # parachains act as application-specific shards
        interoperability="Native XCM (Cross-Consensus Messaging) protocol",
        energy_efficient=True,   # NPoS is PoS-based
        notable_feature="Relay chain + parachain architecture & native XCM",
        avg_tx_fee="<$0.01 (very low; relay chain and parachain fees)",
    )

    print("=" * 80)
    print("           ETHEREUM vs POLKADOT — BLOCKCHAIN COMPARISON")
    print("=" * 80)

    ethereum.display()
    polkadot.display()

    print("\n\n" + "=" * 80)
    print("                        SIDE-BY-SIDE COMPARISON")
    print("=" * 80)
    compare(ethereum, polkadot)

    print("\n\n" + "=" * 80)
    key_differences()

    print("=" * 80)
    use_case_guide()
    print("=" * 80)


if __name__ == "__main__":
    main()
