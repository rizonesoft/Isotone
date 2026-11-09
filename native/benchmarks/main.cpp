// Copyright (C) 2025-2026 Rizonetech (Pty) Ltd. All rights reserved.
// Licensed under the GNU General Public License v3.0 (GPL-3.0-or-later).

#include "benchmarks.h"

#include <benchmark/benchmark.h>
#include <cstdio>
#include <exception>
#include <iostream>
#include <span>
#include <string_view>

int main(int argc, char** argv)
{
    try
    {
        const std::span<char*> args{argv, static_cast<std::size_t>(argc)};
        for (const char* raw_arg : args.subspan(1))
        {
            if (std::string_view{raw_arg} == "--smoke")
            {
                if (!isotone::benchmarks::run_premultiply_smoke_guard())
                {
                    std::cerr << "isotone_benchmarks --smoke: correctness guard failed\n";
                    return 1;
                }
                std::cout << "isotone_benchmarks --smoke: all correctness guards passed\n";
                return 0;
            }
        }

        isotone::benchmarks::register_premultiply_benchmarks();
        benchmark::Initialize(&argc, argv);
        if (benchmark::ReportUnrecognizedArguments(argc, argv))
        {
            return 1;
        }
        benchmark::RunSpecifiedBenchmarks();
        benchmark::Shutdown();
        return 0;
    }
    catch (const std::exception& err)
    {
        (void)std::fputs("isotone_benchmarks: unhandled exception: ", stderr);
        (void)std::fputs(err.what(), stderr);
        (void)std::fputc('\n', stderr);
        return 1;
    }
    catch (...)
    {
        (void)std::fputs("isotone_benchmarks: unhandled unknown exception\n", stderr);
        return 1;
    }
}
