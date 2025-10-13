/*
 * --------------------------------------------------------------------------
 * "THE BEER-WARE LICENSE" (Revision 42):
 * <p-sam@d3vs.net>, <natinusala@gmail.com>, <m4x@m4xw.net>
 * wrote this file. As long as you retain this notice you can do whatever you
 * want with this stuff. If you meet any of us some day, and you think this
 * stuff is worth it, you can buy us a beer in return.  - The sys-clk authors
 * --------------------------------------------------------------------------
 */

/*
 *
 * Copyright (c) Souldbminer and Horizon OC Contributors
 *
 * This program is free software; you can redistribute it and/or modify it
 * under the terms and conditions of the GNU General Public License,
 * version 2, as published by the Free Software Foundation.
 *
 * This program is distributed in the hope it will be useful, but WITHOUT
 * ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
 * FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
 * more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

#pragma once

#include <tesla.hpp>
#include <fstream>
#include <vector>
#include <string>
#include <algorithm>

#include "../style.h"
#include "../../ipc.h"

class BaseGui : public tsl::Gui
{
    public:
        BaseGui() {}
        ~BaseGui() {}
         virtual void preDraw(tsl::gfx::Renderer* renderer);
        void update() override;
        tsl::elm::Element* createUI() override;
        virtual tsl::elm::Element* baseUI() = 0;
        virtual void refresh() {}
    private:
};


extern std::string getVersionString();
